acc1="SRR1219879"
acc2="SRR1219880"
acc3="SRR1257493"
acc4="SRR1257494"

#please substitute for the real public IP of your DRS-server
my_drs="http://XXX.XXX.XXX.XXX"

#please take care of having this file here...
cart="jwt_cart_dbgap_prj_2476_19_years_expiration_date.txt"

clear
python3 drs_request.py $acc1 $my_drs $cart

