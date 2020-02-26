#!/bin/bash

# REMINDER: Must call get_saml_credential.sh and export AWS keys
# Monitor via https://fs.ncbi.nlm.nih.gov/adfs/ls/idpinitiatedsignon

if [ -z "$AWS_ACCESS_KEY_ID" ]; then
    echo "Call get_saml_credential.sh and paste the exports"
    exit
fi

readonly INSTANCE="t3a.micro" # nano doesn't have enough RAM, ~23 cents/day
readonly KEY_NAME=$USER
readonly SUBNET=subnet-4f505738
readonly SGID=sg-5d37473a
# sg-a53e35ce allows 0.0.0.0:8080
# sg-5d37473a allows RDP (3389)
readonly EXPIRES="480" # in minutes

# https://cloud-images.ubuntu.com/locator/ec2/
AMI="ami-00a208c7cdba991ea" # Ubuntu 18.04 LTS, good until 2023-ish

distro="Ubuntu 18.04 LTS"
titledistro="$distro"
login="ubuntu"

declare -A tags
tags["Project"]="VDB"
tags["billingcode"]="VDB"
name="VDB DRS $titledistro Build"
tags["Name"]="$name"
tags["Owner"]=$USER
tags["Created"]=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
tags["Expires"]=$(date -d "+$EXPIRES minutes" -u +"%Y-%m-%dT%H:%M:%SZ")
tags["Creator"]=$(basename "$0")
tags["Description"]="VDB DRS $titledistro builder. Started from $HOSTNAME."

tagstr=""
for key in "${!tags[@]}"; do
    tagstr="{\"Key\":\"${key}\",\"Value\":\"${tags[${key}]}\" },$tagstr"
done
tagstr=${tagstr: : -1} # remove trailing comma

script=$(mktemp --tmpdir aws_scriptXXX)
json=$(mktemp --tmpdir aws_jsonXXX)
#reqout=$(mktemp --tmpdir aws_reqXXX)
#filter=$(mktemp --tmpdir aws_filterXXX)

trap '/bin/rm -f $script $json' INT HUP ALRM EXIT QUIT

cat >> "$script" << ENDSCRIPT
#!/bin/bash
# Output from this script can be found in /var/log/cloud-init-output.log

nohup shutdown -P +$EXPIRES > /tmp/shutdown_out 2>&1  &

sleep 50 # Wait for cloud-init updater to finish

# Add swap
fallocate -l 1G /swap
chmod 600 /swap
mkswap /swap
swapon /swap

sudo apt-mark hold linux-image-generic linux-aws \
    grub-common grub-pc grub-pc-bin grub2-common

sudo apt-get update -y
sudo apt-get upgrade -y
sudo apt-get install -y docker.io python3 python3-pip \
             git shellcheck jq \
             protobuf-compiler

#sudo iptables -A PREROUTING -t nat -i eth0 -p tcp --dport 80 -j REDIRECT --to-port 8080
#sudo iptables -A PREROUTING -t nat -i ens5 -p tcp --dport 80 -j REDIRECT --to-port 8080


sudo usermod -aG docker ubuntu
sudo chmod ugo+w /var/run/docker.sock
ENDSCRIPT
readonly b64json=$(base64 -w 0 "$script")

    #"UserData": "$b64json",
cat > "$json" << ENDJSON
{
    "ImageId": "$AMI",
    "InstanceType": "$INSTANCE",
    "KeyName": "$KEY_NAME",
    "MaxCount": 1,
    "MinCount": 1,
    "Monitoring": { "Enabled": true },
    "SecurityGroupIds": [ "$SGID" ],
    "SubnetId": "$SUBNET",
    "InstanceInitiatedShutdownBehavior": "terminate",
    "TagSpecifications": [
    {
        "ResourceType": "instance",
        "Tags": [
        $tagstr
        ]
    }
    ]
}
ENDJSON


cmd="aws ec2 run-instances \
    --query Instances[0].InstanceId \
    --cli-input-json file://$json \
    --user-data file://$script"
#echo "cmd is $cmd"
instance_id=$($cmd)

instance_id="${instance_id//\"}"

if [ -z "$instance_id" ]
then
    echo "Couldn't start EC2 instance" >&2
    echo -e "Command was:\n\t$cmd\n" >&2
    cat "$json"
    exit 2
fi

echo "$titledistro EC2 instance ID is $instance_id"

# TODO: Add timeout
state=""
while [[ ! $state =~ running ]]
do
    state=$(aws ec2 describe-instances --instance-ids "$instance_id"  | jq -r '.Reservations[0].Instances[0].State.Name')
    echo "  State of $instance_id is: $state"
    sleep 5
done


ret=1
while [[ $ret -ne 0 ]]
do
    sleep 20

    ip_addr=$(aws ec2 describe-instances --instance-ids "$instance_id" | jq -r '.Reservations[0].Instances[0].PublicIpAddress')
    echo "  EC2 IP Address is $ip_addr"
    echo "  Waiting for instance to start sshd ..."
    nc -w 2 "$ip_addr" 22 < /dev/null > /dev/null 2>&1
    ret=$?
done

sleep 240
scp ./*require*.txt "$login@$ip_addr:/tmp/"
ssh -2akx "$login@$ip_addr" 'git clone https://github.com/ncbi/ncbi-drs/'
scp /home/vartanianmh/jenkins_drs.tar "$login@$ip_addr:ncbi-drs/jenkins.tar"
ssh -2akx "$login@$ip_addr" 'pip3 -q install -r /tmp/requirements.txt -r /tmp/test-requirements.txt'
ssh -2akx "$login@$ip_addr" 'cd ncbi-drs && ~/.local/bin/pre-commit install'

BRANCH_NAME=$(git symbolic-ref --short HEAD)

echo "Run:"
echo " ssh -2akx $login@$ip_addr"
echo " cd ncbi-drs"
echo " git checkout $BRANCH_NAME"
echo " docker build -t jenkins -f jenkins/Dockerfile ."
echo " docker run --network host --detach --volume /var/run/docker.sock:/var/run/docker.sock jenkins"
echo " sudo iptables -A PREROUTING -t nat -i eth0 -p tcp --dport 443 -j REDIRECT --to-port 8080"
echo " sudo iptables -A PREROUTING -t nat -i ens5 -p tcp --dport 443 -j REDIRECT --to-port 8080"

echo " and then Jenkins should be running on http://$ip_addr:443/"
