# =============================================================================
#
#                            PUBLIC DOMAIN NOTICE
#               National Center for Biotechnology Information
#
#  This software/database is a "United States Government Work" under the
#  terms of the United States Copyright Act.  It was written as part of
#  the author's official duties as a United States Government employee and
#  thus cannot be copyrighted.  This software/database is freely available
#  to the public for use. The National Library of Medicine and the U.S.
#  Government have not placed any restriction on its use or reproduction.
#
#  Although all reasonable efforts have been taken to ensure the accuracy
#  and reliability of the software and data, the NLM and the U.S.
#  Government do not and cannot warrant the performance or results that
#  may be obtained by using this software or data. The NLM and the U.S.
#  Government disclaim all warranties, express or implied, including
#  warranties of performance, merchantability or fitness for any particular
#  purpose.
#
#  Please cite the author in any work or product based on this material.
#
# =============================================================================
#

""" Provide test values for unit-testing of server.py """

response_ok = """
{
    "version": "2",
    "result": [
        {
            "bundle": "SRR10039049",
            "status": 200,
            "msg": "ok",
            "files": [
                {
                    "object": "remote|SRR10039049",
                    "type": "bam/gzip",
                    "name": "f4.f.mscs.DMSO5.meth.merged.sorted.uniq.bam",
                    "size": 2299145289,
                    "md5": "aa8fbf47c010ee82e783f52f9e7a21d0",
                    "modificationDate": "2019-08-30T15:21:11Z",
                    "locations": [
                        {
                            "link": "https://sra-pub-src-2.s3.amazonaws.com/SRR10039049/f4.f.mscs.DMSO5.meth.merged.sorted.uniq.bam.1",
                            "service": "s3",
                            "region": "us-east-1"
                        }
                    ]
                }
            ]
        }
    ]
}
"""

bad_version = """
{
    "version": "unstable",
    "result": [
        {
            "bundle": "SRR10039049",
            "status": 200,
            "msg": "ok",
            "files": [
                {
                    "object": "remote|SRR10039049",
                    "type": "bam/gzip",
                    "name": "f4.f.mscs.DMSO5.meth.merged.sorted.uniq.bam",
                    "size": 2299145289,
                    "md5": "aa8fbf47c010ee82e783f52f9e7a21d0",
                    "modificationDate": "2019-08-30T15:21:11Z",
                    "locations": [
                        {
                            "link": "https://sra-pub-src-2.s3.amazonaws.com/SRR10039049/f4.f.mscs.DMSO5.meth.merged.sorted.uniq.bam.1",
                            "service": "s3",
                            "region": "us-east-1"
                        }
                    ]
                }
            ]
        }
    ]
}
"""

response_404 = """
{
    "version": "2",
    "result": [
        {
            "bundle": "SRR10039049",
            "status": 404,
            "msg": "Cannot resolve accession"
        }
    ]
}
"""

response_500 = """
{
    "status": 500,
    "message": "No accession to process"
}
"""

response_SRP219736 = """
{
    "version": "2",
    "result": [
        {
            "bundle": "SRP219736",
            "status": 200,
            "msg": "ok",
            "files": [
                {
                    "object": "remote|SRR10039019",
                    "type": "bam/gzip",
                    "name": "f4.m.liv.DMSO3.rna.merged.sorted.bam",
                    "size": 997509443,
                    "md5": "b5f36d2cb27a3cdf05d286ec9f346387",
                    "modificationDate": "2019-08-30T15:04:10Z",
                    "locations": [
                        {
                            "link": "https://sra-pub-src-2.s3.amazonaws.com/SRR10039019/f4.m.liv.DMSO3.rna.merged.sorted.bam.1",
                            "service": "s3",
                            "region": "us-east-1"
                        }
                    ]
                },
                {
                    "object": "remote|SRR10039017",
                    "type": "bam/gzip",
                    "name": "f4.m.liv.DMSO1.rna.merged.sorted.bam",
                    "size": 1128363105,
                    "md5": "02b1ea5174fee52d14195fd07ece176a",
                    "modificationDate": "2019-08-30T15:04:29Z",
                    "locations": [
                        {
                            "link": "https://sra-pub-src-2.s3.amazonaws.com/SRR10039017/f4.m.liv.DMSO1.rna.merged.sorted.bam.1",
                            "service": "s3",
                            "region": "us-east-1"
                        }
                    ]
                },
                {
                    "object": "remote|SRR10039018",
                    "type": "bam/gzip",
                    "name": "f4.m.liv.DMSO2.rna.merged.sorted.bam",
                    "size": 1150871673,
                    "md5": "d299d3fb4d884ea7f3804140d844356f",
                    "modificationDate": "2019-08-30T15:04:39Z",
                    "locations": [
                        {
                            "link": "https://sra-pub-src-2.s3.amazonaws.com/SRR10039018/f4.m.liv.DMSO2.rna.merged.sorted.bam.1",
                            "service": "s3",
                            "region": "us-east-1"
                        }
                    ]
                },
                {
                    "object": "remote|SRR10039020",
                    "type": "bam/gzip",
                    "name": "f4.m.liv.DMSO4.rna.merged.sorted.bam",
                    "size": 1141422286,
                    "md5": "7db88dde950fd5accfae214fc0183b1b",
                    "modificationDate": "2019-08-30T15:04:34Z",
                    "locations": [
                        {
                            "link": "https://sra-pub-src-2.s3.amazonaws.com/SRR10039020/f4.m.liv.DMSO4.rna.merged.sorted.bam.1",
                            "service": "s3",
                            "region": "us-east-1"
                        }
                    ]
                },
                {
                    "object": "remote|SRR10039021",
                    "type": "bam/gzip",
                    "name": "f4.m.liv.TBT1.rna.merged.sorted.bam",
                    "size": 1281139288,
                    "md5": "8de2af92d19d0a98be28a4cf08b7806f",
                    "modificationDate": "2019-08-30T15:05:19Z",
                    "locations": [
                        {
                            "link": "https://sra-pub-src-2.s3.amazonaws.com/SRR10039021/f4.m.liv.TBT1.rna.merged.sorted.bam.1",
                            "service": "s3",
                            "region": "us-east-1"
                        }
                    ]
                },
                {
                    "object": "remote|SRR10039024",
                    "type": "bam/gzip",
                    "name": "f4.m.liv.TBT4.rna.merged.sorted.bam",
                    "size": 1764948608,
                    "md5": "cbf19ace9a7bba3fd380d49887713dda",
                    "modificationDate": "2019-08-30T15:06:04Z",
                    "locations": [
                        {
                            "link": "https://sra-pub-src-2.s3.amazonaws.com/SRR10039024/f4.m.liv.TBT4.rna.merged.sorted.bam.1",
                            "service": "s3",
                            "region": "us-east-1"
                        }
                    ]
                },
                {
                    "object": "remote|SRR10039023",
                    "type": "bam/gzip",
                    "name": "f4.m.liv.TBT3.rna.merged.sorted.bam",
                    "size": 1754252237,
                    "md5": "5f69326e69ebef907b238caedd6ba635",
                    "modificationDate": "2019-08-30T15:07:02Z",
                    "locations": [
                        {
                            "link": "https://sra-pub-src-2.s3.amazonaws.com/SRR10039023/f4.m.liv.TBT3.rna.merged.sorted.bam.1",
                            "service": "s3",
                            "region": "us-east-1"
                        }
                    ]
                },
                {
                    "object": "remote|SRR10038996",
                    "type": "bam/gzip",
                    "name": "f3.m.mscs.TBT5.rna.merged.sorted.bam",
                    "size": 1809406139,
                    "md5": "3a3f3bddc53c0f475c8c8cc5b0d5fbdf",
                    "modificationDate": "2019-08-30T15:07:43Z",
                    "locations": [
                        {
                            "link": "https://sra-pub-src-2.s3.amazonaws.com/SRR10038996/f3.m.mscs.TBT5.rna.merged.sorted.bam.1",
                            "service": "s3",
                            "region": "us-east-1"
                        }
                    ]
                },
                {
                    "object": "remote|SRR10038985",
                    "type": "bam/gzip",
                    "name": "f3.f.mscs.TBT4.rna.merged.sorted.bam",
                    "size": 1716318341,
                    "md5": "65f0d4d4fceb40cc33ea88470b157256",
                    "modificationDate": "2019-08-30T15:07:50Z",
                    "locations": [
                        {
                            "link": "https://sra-pub-src-2.s3.amazonaws.com/SRR10038985/f3.f.mscs.TBT4.rna.merged.sorted.bam.1",
                            "service": "s3",
                            "region": "us-east-1"
                        }
                    ]
                },
                {
                    "object": "remote|SRR10039070",
                    "type": "bam/gzip",
                    "name": "f4.m.liv.TBT2.meth.merged.sorted.uniq.bam",
                    "size": 1181350236,
                    "md5": "a1fc66be6830f6a5e6ec2cc4b7fbb767",
                    "modificationDate": "2019-08-30T15:08:15Z",
                    "locations": [
                        {
                            "link": "https://sra-pub-src-2.s3.amazonaws.com/SRR10039070/f4.m.liv.TBT2.meth.merged.sorted.uniq.bam.1",
                            "service": "s3",
                            "region": "us-east-1"
                        }
                    ]
                },
                {
                    "object": "remote|SRR10038978",
                    "type": "bam/gzip",
                    "name": "f3.f.mscs.DMSO2.rna.merged.sorted.bam",
                    "size": 1796764438,
                    "md5": "2b61cf8b815309a2c8e57a5b5563b83f",
                    "modificationDate": "2019-08-30T15:07:59Z",
                    "locations": [
                        {
                            "link": "https://sra-pub-src-2.s3.amazonaws.com/SRR10038978/f3.f.mscs.DMSO2.rna.merged.sorted.bam.1",
                            "service": "s3",
                            "region": "us-east-1"
                        }
                    ]
                },
                {
                    "object": "remote|SRR10039027",
                    "type": "bam/gzip",
                    "name": "f3.f.mscs.DMSO3.meth.merged.sorted.uniq.bam",
                    "size": 1022854530,
                    "md5": "b1279e493849d6520410ac99f7c0f5df",
                    "modificationDate": "2019-08-30T15:08:40Z",
                    "locations": [
                        {
                            "link": "https://sra-pub-src-2.s3.amazonaws.com/SRR10039027/f3.f.mscs.DMSO3.meth.merged.sorted.uniq.bam.1",
                            "service": "s3",
                            "region": "us-east-1"
                        }
                    ]
                },
                {
                    "object": "remote|SRR10038984",
                    "type": "bam/gzip",
                    "name": "f3.f.mscs.TBT3.rna.merged.sorted.bam",
                    "size": 1796211459,
                    "md5": "f4ab5b51cf68d2040e3647e7e386f746",
                    "modificationDate": "2019-08-30T15:08:23Z",
                    "locations": [
                        {
                            "link": "https://sra-pub-src-2.s3.amazonaws.com/SRR10038984/f3.f.mscs.TBT3.rna.merged.sorted.bam.1",
                            "service": "s3",
                            "region": "us-east-1"
                        }
                    ]
                },
                {
                    "object": "remote|SRR10038980",
                    "type": "bam/gzip",
                    "name": "f3.f.mscs.DMSO4.rna.merged.sorted.bam",
                    "size": 1586462251,
                    "md5": "bb1140892eb5e16da6e0507127cc5148",
                    "modificationDate": "2019-08-30T15:08:26Z",
                    "locations": [
                        {
                            "link": "https://sra-pub-src-2.s3.amazonaws.com/SRR10038980/f3.f.mscs.DMSO4.rna.merged.sorted.bam.1",
                            "service": "s3",
                            "region": "us-east-1"
                        }
                    ]
                },
                {
                    "object": "remote|SRR10038989",
                    "type": "bam/gzip",
                    "name": "f3.m.mscs.DMSO3.rna.merged.sorted.bam",
                    "size": 1968263175,
                    "md5": "6cac4c8983ee2c340e7b09de9ec4ba30",
                    "modificationDate": "2019-08-30T15:08:08Z",
                    "locations": [
                        {
                            "link": "https://sra-pub-src-2.s3.amazonaws.com/SRR10038989/f3.m.mscs.DMSO3.rna.merged.sorted.bam.1",
                            "service": "s3",
                            "region": "us-east-1"
                        }
                    ]
                },
                {
                    "object": "remote|SRR10039029",
                    "type": "bam/gzip",
                    "name": "f3.f.mscs.DMSO5.meth.merged.sorted.uniq.bam",
                    "size": 1260019714,
                    "md5": "39380b191262cbe7679c8a951aa5a897",
                    "modificationDate": "2019-08-30T15:09:07Z",
                    "locations": [
                        {
                            "link": "https://sra-pub-src-2.s3.amazonaws.com/SRR10039029/f3.f.mscs.DMSO5.meth.merged.sorted.uniq.bam.1",
                            "service": "s3",
                            "region": "us-east-1"
                        }
                    ]
                },
                {
                    "object": "remote|SRR10038988",
                    "type": "bam/gzip",
                    "name": "f3.m.mscs.DMSO2.rna.merged.sorted.bam",
                    "size": 1881955283,
                    "md5": "7e0822f441bf035c54b55d4a2f8798cb",
                    "modificationDate": "2019-08-30T15:08:52Z",
                    "locations": [
                        {
                            "link": "https://sra-pub-src-2.s3.amazonaws.com/SRR10038988/f3.m.mscs.DMSO2.rna.merged.sorted.bam.1",
                            "service": "s3",
                            "region": "us-east-1"
                        }
                    ]
                },
                {
                    "object": "remote|SRR10038986",
                    "type": "bam/gzip",
                    "name": "f3.f.mscs.TBT5.rna.merged.sorted.bam",
                    "size": 1787879083,
                    "md5": "b1881b7d9ee169d5e00f9fbc14e1c183",
                    "modificationDate": "2019-08-30T15:09:06Z",
                    "locations": [
                        {
                            "link": "https://sra-pub-src-2.s3.amazonaws.com/SRR10038986/f3.f.mscs.TBT5.rna.merged.sorted.bam.1",
                            "service": "s3",
                            "region": "us-east-1"
                        }
                    ]
                },
                {
                    "object": "remote|SRR10038993",
                    "type": "bam/gzip",
                    "name": "f3.m.mscs.TBT2.rna.merged.sorted.bam",
                    "size": 1931999572,
                    "md5": "c5089bc78e5d1b61f29a12f03ccfa517",
                    "modificationDate": "2019-08-30T15:09:12Z",
                    "locations": [
                        {
                            "link": "https://sra-pub-src-2.s3.amazonaws.com/SRR10038993/f3.m.mscs.TBT2.rna.merged.sorted.bam.1",
                            "service": "s3",
                            "region": "us-east-1"
                        }
                    ]
                },
                {
                    "object": "remote|SRR10038982",
                    "type": "bam/gzip",
                    "name": "f3.f.mscs.TBT1.rna.merged.sorted.bam",
                    "size": 1875245438,
                    "md5": "d5fd2de51db3014166cc28f86c8feb3c",
                    "modificationDate": "2019-08-30T15:09:20Z",
                    "locations": [
                        {
                            "link": "https://sra-pub-src-2.s3.amazonaws.com/SRR10038982/f3.f.mscs.TBT1.rna.merged.sorted.bam.1",
                            "service": "s3",
                            "region": "us-east-1"
                        }
                    ]
                },
                {
                    "object": "remote|SRR10038995",
                    "type": "bam/gzip",
                    "name": "f3.m.mscs.TBT4.rna.merged.sorted.bam",
                    "size": 2057392597,
                    "md5": "570a53187957db4fd813fc47d5b06f5c",
                    "modificationDate": "2019-08-30T15:09:44Z",
                    "locations": [
                        {
                            "link": "https://sra-pub-src-2.s3.amazonaws.com/SRR10038995/f3.m.mscs.TBT4.rna.merged.sorted.bam.1",
                            "service": "s3",
                            "region": "us-east-1"
                        }
                    ]
                },
                {
                    "object": "remote|SRR10038994",
                    "type": "bam/gzip",
                    "name": "f3.m.mscs.TBT3.rna.merged.sorted.bam",
                    "size": 2014549331,
                    "md5": "4dcced3dd4c2abed62043187af510514",
                    "modificationDate": "2019-08-30T15:09:45Z",
                    "locations": [
                        {
                            "link": "https://sra-pub-src-2.s3.amazonaws.com/SRR10038994/f3.m.mscs.TBT3.rna.merged.sorted.bam.1",
                            "service": "s3",
                            "region": "us-east-1"
                        }
                    ]
                },
                {
                    "object": "remote|SRR10038983",
                    "type": "bam/gzip",
                    "name": "f3.f.mscs.TBT2.rna.merged.sorted.bam",
                    "size": 2121353376,
                    "md5": "b724438b02070ed5bd8ea7bcf18c1d4b",
                    "modificationDate": "2019-08-30T15:09:56Z",
                    "locations": [
                        {
                            "link": "https://sra-pub-src-2.s3.amazonaws.com/SRR10038983/f3.f.mscs.TBT2.rna.merged.sorted.bam.1",
                            "service": "s3",
                            "region": "us-east-1"
                        }
                    ]
                },
                {
                    "object": "remote|SRR10039030",
                    "type": "bam/gzip",
                    "name": "f3.f.mscs.TBT1.meth.merged.sorted.uniq.bam",
                    "size": 1215483417,
                    "md5": "4aac954e7c2fe6902d71e63757b876cf",
                    "modificationDate": "2019-08-30T15:10:29Z",
                    "locations": [
                        {
                            "link": "https://sra-pub-src-2.s3.amazonaws.com/SRR10039030/f3.f.mscs.TBT1.meth.merged.sorted.uniq.bam.1",
                            "service": "s3",
                            "region": "us-east-1"
                        }
                    ]
                },
                {
                    "object": "remote|SRR10038979",
                    "type": "bam/gzip",
                    "name": "f3.f.mscs.DMSO3.rna.merged.sorted.bam",
                    "size": 2139816554,
                    "md5": "f431d27d1380417424156a49d1b43ca2",
                    "modificationDate": "2019-08-30T15:10:00Z",
                    "locations": [
                        {
                            "link": "https://sra-pub-src-2.s3.amazonaws.com/SRR10038979/f3.f.mscs.DMSO3.rna.merged.sorted.bam.1",
                            "service": "s3",
                            "region": "us-east-1"
                        }
                    ]
                },
                {
                    "object": "remote|SRR10039033",
                    "type": "bam/gzip",
                    "name": "f3.f.mscs.TBT4.meth.merged.sorted.uniq.bam",
                    "size": 1282850513,
                    "md5": "2085e67ac7630852b627aca200f72bbc",
                    "modificationDate": "2019-08-30T15:10:33Z",
                    "locations": [
                        {
                            "link": "https://sra-pub-src-2.s3.amazonaws.com/SRR10039033/f3.f.mscs.TBT4.meth.merged.sorted.uniq.bam.1",
                            "service": "s3",
                            "region": "us-east-1"
                        }
                    ]
                },
                {
                    "object": "remote|SRR10038991",
                    "type": "bam/gzip",
                    "name": "f3.m.mscs.DMSO5.rna.merged.sorted.bam",
                    "size": 2223556560,
                    "md5": "01a4d814f14630c3b97444e1e1bc42ea",
                    "modificationDate": "2019-08-30T15:10:19Z",
                    "locations": [
                        {
                            "link": "https://sra-pub-src-2.s3.amazonaws.com/SRR10038991/f3.m.mscs.DMSO5.rna.merged.sorted.bam.1",
                            "service": "s3",
                            "region": "us-east-1"
                        }
                    ]
                },
                {
                    "object": "remote|SRR10038990",
                    "type": "bam/gzip",
                    "name": "f3.m.mscs.DMSO4.rna.merged.sorted.bam",
                    "size": 1858416956,
                    "md5": "1c3304413bda1d0ee73516e919d3b1a9",
                    "modificationDate": "2019-08-30T15:10:37Z",
                    "locations": [
                        {
                            "link": "https://sra-pub-src-2.s3.amazonaws.com/SRR10038990/f3.m.mscs.DMSO4.rna.merged.sorted.bam.1",
                            "service": "s3",
                            "region": "us-east-1"
                        }
                    ]
                },
                {
                    "object": "remote|SRR10039071",
                    "type": "bam/gzip",
                    "name": "f4.m.liv.TBT3.meth.merged.sorted.uniq.bam",
                    "size": 1190401817,
                    "md5": "3ff1b34bb0c39c0e132d81cc678fc753",
                    "modificationDate": "2019-08-30T15:11:17Z",
                    "locations": [
                        {
                            "link": "https://sra-pub-src-2.s3.amazonaws.com/SRR10039071/f4.m.liv.TBT3.meth.merged.sorted.uniq.bam.1",
                            "service": "s3",
                            "region": "us-east-1"
                        }
                    ]
                },
                {
                    "object": "remote|SRR10038981",
                    "type": "bam/gzip",
                    "name": "f3.f.mscs.DMSO5.rna.merged.sorted.bam",
                    "size": 1750409161,
                    "md5": "54ff4f81ac2db51fc8a2ee5453eb4696",
                    "modificationDate": "2019-08-30T15:11:20Z",
                    "locations": [
                        {
                            "link": "https://sra-pub-src-2.s3.amazonaws.com/SRR10038981/f3.f.mscs.DMSO5.rna.merged.sorted.bam.1",
                            "service": "s3",
                            "region": "us-east-1"
                        }
                    ]
                },
                {
                    "object": "remote|SRR10039037",
                    "type": "bam/gzip",
                    "name": "f3.m.mscs.DMSO3.meth.merged.sorted.uniq.bam",
                    "size": 1223742974,
                    "md5": "6e3a68c6b51b5d5cbe95a13488dc142b",
                    "modificationDate": "2019-08-30T15:11:46Z",
                    "locations": [
                        {
                            "link": "https://sra-pub-src-2.s3.amazonaws.com/SRR10039037/f3.m.mscs.DMSO3.meth.merged.sorted.uniq.bam.1",
                            "service": "s3",
                            "region": "us-east-1"
                        }
                    ]
                },
                {
                    "object": "remote|SRR10039032",
                    "type": "bam/gzip",
                    "name": "f3.f.mscs.TBT3.meth.merged.sorted.uniq.bam",
                    "size": 1468610032,
                    "md5": "b5e89365fa4cb5dd7fece70716679df6",
                    "modificationDate": "2019-08-30T15:11:46Z",
                    "locations": [
                        {
                            "link": "https://sra-pub-src-2.s3.amazonaws.com/SRR10039032/f3.f.mscs.TBT3.meth.merged.sorted.uniq.bam.1",
                            "service": "s3",
                            "region": "us-east-1"
                        }
                    ]
                },
                {
                    "object": "remote|SRR10039038",
                    "type": "bam/gzip",
                    "name": "f3.m.mscs.DMSO4.meth.merged.sorted.uniq.bam",
                    "size": 1197411167,
                    "md5": "02a65cc292a0af87e956c4de400f8ce6",
                    "modificationDate": "2019-08-30T15:12:04Z",
                    "locations": [
                        {
                            "link": "https://sra-pub-src-2.s3.amazonaws.com/SRR10039038/f3.m.mscs.DMSO4.meth.merged.sorted.uniq.bam.1",
                            "service": "s3",
                            "region": "us-east-1"
                        }
                    ]
                },
                {
                    "object": "remote|SRR10039072",
                    "type": "bam/gzip",
                    "name": "f4.m.liv.TBT4.meth.merged.sorted.uniq.bam",
                    "size": 1418371685,
                    "md5": "a60834af381e654676676f39ffb7b663",
                    "modificationDate": "2019-08-30T15:11:56Z",
                    "locations": [
                        {
                            "link": "https://sra-pub-src-2.s3.amazonaws.com/SRR10039072/f4.m.liv.TBT4.meth.merged.sorted.uniq.bam.1",
                            "service": "s3",
                            "region": "us-east-1"
                        }
                    ]
                },
                {
                    "object": "remote|SRR10038977",
                    "type": "bam/gzip",
                    "name": "f3.f.mscs.DMSO1.rna.merged.sorted.bam",
                    "size": 2423409915,
                    "md5": "9d1ff6c745620397383d446fc792a43d",
                    "modificationDate": "2019-08-30T15:11:32Z",
                    "locations": [
                        {
                            "link": "https://sra-pub-src-2.s3.amazonaws.com/SRR10038977/f3.f.mscs.DMSO1.rna.merged.sorted.bam.1",
                            "service": "s3",
                            "region": "us-east-1"
                        }
                    ]
                },
                {
                    "object": "remote|SRR10039034",
                    "type": "bam/gzip",
                    "name": "f3.f.mscs.TBT5.meth.merged.sorted.uniq.bam",
                    "size": 1303458617,
                    "md5": "8157936cbf40d5255d0d394948f88bcd",
                    "modificationDate": "2019-08-30T15:12:06Z",
                    "locations": [
                        {
                            "link": "https://sra-pub-src-2.s3.amazonaws.com/SRR10039034/f3.f.mscs.TBT5.meth.merged.sorted.uniq.bam.1",
                            "service": "s3",
                            "region": "us-east-1"
                        }
                    ]
                },
                {
                    "object": "remote|SRR10039031",
                    "type": "bam/gzip",
                    "name": "f3.f.mscs.TBT2.meth.merged.sorted.uniq.bam",
                    "size": 1441260371,
                    "md5": "68ba4e38b4e1ad683a8adbaec0f69ef5",
                    "modificationDate": "2019-08-30T15:12:33Z",
                    "locations": [
                        {
                            "link": "https://sra-pub-src-2.s3.amazonaws.com/SRR10039031/f3.f.mscs.TBT2.meth.merged.sorted.uniq.bam.1",
                            "service": "s3",
                            "region": "us-east-1"
                        }
                    ]
                },
                {
                    "object": "remote|SRR10038987",
                    "type": "bam/gzip",
                    "name": "f3.m.mscs.DMSO1.rna.merged.sorted.bam",
                    "size": 2474458515,
                    "md5": "36f0ba3c12b5694b2fb4d2c07aeefd53",
                    "modificationDate": "2019-08-30T15:12:14Z",
                    "locations": [
                        {
                            "link": "https://sra-pub-src-2.s3.amazonaws.com/SRR10038987/f3.m.mscs.DMSO1.rna.merged.sorted.bam.1",
                            "service": "s3",
                            "region": "us-east-1"
                        }
                    ]
                },
                {
                    "object": "remote|SRR10039069",
                    "type": "bam/gzip",
                    "name": "f4.m.liv.TBT1.meth.merged.sorted.uniq.bam",
                    "size": 1410089135,
                    "md5": "e1968c18576ef209bdb1c5cfa2aac35f",
                    "modificationDate": "2019-08-30T15:12:41Z",
                    "locations": [
                        {
                            "link": "https://sra-pub-src-2.s3.amazonaws.com/SRR10039069/f4.m.liv.TBT1.meth.merged.sorted.uniq.bam.1",
                            "service": "s3",
                            "region": "us-east-1"
                        }
                    ]
                },
                {
                    "object": "remote|SRR10039065",
                    "type": "bam/gzip",
                    "name": "f4.m.liv.DMSO1.meth.merged.sorted.uniq.bam",
                    "size": 1575326769,
                    "md5": "297d907b9ef5e8b82ba9aa5b423b4162",
                    "modificationDate": "2019-08-30T15:13:11Z",
                    "locations": [
                        {
                            "link": "https://sra-pub-src-2.s3.amazonaws.com/SRR10039065/f4.m.liv.DMSO1.meth.merged.sorted.uniq.bam.1",
                            "service": "s3",
                            "region": "us-east-1"
                        }
                    ]
                },
                {
                    "object": "remote|SRR10039025",
                    "type": "bam/gzip",
                    "name": "f3.f.mscs.DMSO1.meth.merged.sorted.uniq.bam",
                    "size": 1433517223,
                    "md5": "39f7b1f82c89954803b875cfeb9d54d4",
                    "modificationDate": "2019-08-30T15:13:52Z",
                    "locations": [
                        {
                            "link": "https://sra-pub-src-2.s3.amazonaws.com/SRR10039025/f3.f.mscs.DMSO1.meth.merged.sorted.uniq.bam.1",
                            "service": "s3",
                            "region": "us-east-1"
                        }
                    ]
                },
                {
                    "object": "remote|SRR10039067",
                    "type": "bam/gzip",
                    "name": "f4.m.liv.DMSO3.meth.merged.sorted.uniq.bam",
                    "size": 1732749456,
                    "md5": "c0befadbbb0f28bac9ac6e6eb8c4c53a",
                    "modificationDate": "2019-08-30T15:13:45Z",
                    "locations": [
                        {
                            "link": "https://sra-pub-src-2.s3.amazonaws.com/SRR10039067/f4.m.liv.DMSO3.meth.merged.sorted.uniq.bam.1",
                            "service": "s3",
                            "region": "us-east-1"
                        }
                    ]
                },
                {
                    "object": "remote|SRR10039059",
                    "type": "bam/gzip",
                    "name": "f4.m.mscs.DMSO5.meth.merged.sorted.uniq.bam",
                    "size": 1797332777,
                    "md5": "a178dbf7e5d7d330291e9f2782ad36f4",
                    "modificationDate": "2019-08-30T15:14:01Z",
                    "locations": [
                        {
                            "link": "https://sra-pub-src-2.s3.amazonaws.com/SRR10039059/f4.m.mscs.DMSO5.meth.merged.sorted.uniq.bam.1",
                            "service": "s3",
                            "region": "us-east-1"
                        }
                    ]
                },
                {
                    "object": "remote|SRR10039042",
                    "type": "bam/gzip",
                    "name": "f3.m.mscs.TBT3.meth.merged.sorted.uniq.bam",
                    "size": 1592701429,
                    "md5": "3e0c08189c846e91ed12689fc9f52c3a",
                    "modificationDate": "2019-08-30T15:14:02Z",
                    "locations": [
                        {
                            "link": "https://sra-pub-src-2.s3.amazonaws.com/SRR10039042/f3.m.mscs.TBT3.meth.merged.sorted.uniq.bam.1",
                            "service": "s3",
                            "region": "us-east-1"
                        }
                    ]
                },
                {
                    "object": "remote|SRR10039068",
                    "type": "bam/gzip",
                    "name": "f4.m.liv.DMSO4.meth.merged.sorted.uniq.bam",
                    "size": 1272467438,
                    "md5": "ebdd8a6647eb094541145d1724a9b784",
                    "modificationDate": "2019-08-30T15:14:26Z",
                    "locations": [
                        {
                            "link": "https://sra-pub-src-2.s3.amazonaws.com/SRR10039068/f4.m.liv.DMSO4.meth.merged.sorted.uniq.bam.1",
                            "service": "s3",
                            "region": "us-east-1"
                        }
                    ]
                },
                {
                    "object": "remote|SRR10039054",
                    "type": "bam/gzip",
                    "name": "f4.f.mscs.TBT5.meth.merged.sorted.uniq.bam",
                    "size": 2154876211,
                    "md5": "596b59f047dde490cf216557d9fa42e6",
                    "modificationDate": "2019-08-30T15:14:41Z",
                    "locations": [
                        {
                            "link": "https://sra-pub-src-2.s3.amazonaws.com/SRR10039054/f4.f.mscs.TBT5.meth.merged.sorted.uniq.bam.1",
                            "service": "s3",
                            "region": "us-east-1"
                        }
                    ]
                },
                {
                    "object": "remote|SRR10039028",
                    "type": "bam/gzip",
                    "name": "f3.f.mscs.DMSO4.meth.merged.sorted.uniq.bam",
                    "size": 1347360889,
                    "md5": "45a84aae86da13f47bdd4f2164bf8350",
                    "modificationDate": "2019-08-30T15:14:37Z",
                    "locations": [
                        {
                            "link": "https://sra-pub-src-2.s3.amazonaws.com/SRR10039028/f3.f.mscs.DMSO4.meth.merged.sorted.uniq.bam.1",
                            "service": "s3",
                            "region": "us-east-1"
                        }
                    ]
                },
                {
                    "object": "remote|SRR10039041",
                    "type": "bam/gzip",
                    "name": "f3.m.mscs.TBT2.meth.merged.sorted.uniq.bam",
                    "size": 1668531760,
                    "md5": "af42a8464dee642e28e7d2c85303f82b",
                    "modificationDate": "2019-08-30T15:14:45Z",
                    "locations": [
                        {
                            "link": "https://sra-pub-src-2.s3.amazonaws.com/SRR10039041/f3.m.mscs.TBT2.meth.merged.sorted.uniq.bam.1",
                            "service": "s3",
                            "region": "us-east-1"
                        }
                    ]
                },
                {
                    "object": "remote|SRR10038992",
                    "type": "bam/gzip",
                    "name": "f3.m.mscs.TBT1.rna.merged.sorted.bam",
                    "size": 2972860826,
                    "md5": "60fcca602aa30299538b709970c9eba0",
                    "modificationDate": "2019-08-30T15:14:25Z",
                    "locations": [
                        {
                            "link": "https://sra-pub-src-2.s3.amazonaws.com/SRR10038992/f3.m.mscs.TBT1.rna.merged.sorted.bam.1",
                            "service": "s3",
                            "region": "us-east-1"
                        }
                    ]
                },
                {
                    "object": "remote|SRR10039057",
                    "type": "bam/gzip",
                    "name": "f4.m.mscs.DMSO3.meth.merged.sorted.uniq.bam",
                    "size": 2275624827,
                    "md5": "6f72b124c19469166575b8e01c955821",
                    "modificationDate": "2019-08-30T15:15:01Z",
                    "locations": [
                        {
                            "link": "https://sra-pub-src-2.s3.amazonaws.com/SRR10039057/f4.m.mscs.DMSO3.meth.merged.sorted.uniq.bam.1",
                            "service": "s3",
                            "region": "us-east-1"
                        }
                    ]
                },
                {
                    "object": "remote|SRR10039006",
                    "type": "bam/gzip",
                    "name": "f4.f.mscs.TBT5.rna.merged.sorted.bam",
                    "size": 4176561977,
                    "md5": "f01f52a5875698fcb34d4eb2e6fc0b8a",
                    "modificationDate": "2019-08-30T15:14:36Z",
                    "locations": [
                        {
                            "link": "https://sra-pub-src-2.s3.amazonaws.com/SRR10039006/f4.f.mscs.TBT5.rna.merged.sorted.bam.1",
                            "service": "s3",
                            "region": "us-east-1"
                        }
                    ]
                },
                {
                    "object": "remote|SRR10039005",
                    "type": "bam/gzip",
                    "name": "f4.f.mscs.TBT4.rna.merged.sorted.bam",
                    "size": 3701988346,
                    "md5": "b5371e80ffdef7248fabed4b9b126514",
                    "modificationDate": "2019-08-30T15:14:27Z",
                    "locations": [
                        {
                            "link": "https://sra-pub-src-2.s3.amazonaws.com/SRR10039005/f4.f.mscs.TBT4.rna.merged.sorted.bam.1",
                            "service": "s3",
                            "region": "us-east-1"
                        }
                    ]
                },
                {
                    "object": "remote|SRR10039039",
                    "type": "bam/gzip",
                    "name": "f3.m.mscs.DMSO5.meth.merged.sorted.uniq.bam",
                    "size": 1308382926,
                    "md5": "5776bdbeea08f1527894fd145e9390e2",
                    "modificationDate": "2019-08-30T15:15:45Z",
                    "locations": [
                        {
                            "link": "https://sra-pub-src-2.s3.amazonaws.com/SRR10039039/f3.m.mscs.DMSO5.meth.merged.sorted.uniq.bam.1",
                            "service": "s3",
                            "region": "us-east-1"
                        }
                    ]
                },
                {
                    "object": "remote|SRR10039066",
                    "type": "bam/gzip",
                    "name": "f4.m.liv.DMSO2.meth.merged.sorted.uniq.bam",
                    "size": 1725332130,
                    "md5": "69e748e5301327ad6a266b3a443f938f",
                    "modificationDate": "2019-08-30T15:15:34Z",
                    "locations": [
                        {
                            "link": "https://sra-pub-src-2.s3.amazonaws.com/SRR10039066/f4.m.liv.DMSO2.meth.merged.sorted.uniq.bam.1",
                            "service": "s3",
                            "region": "us-east-1"
                        }
                    ]
                },
                {
                    "object": "remote|SRR10039008",
                    "type": "bam/gzip",
                    "name": "f4.m.mscs.DMSO2.rna.merged.sorted.bam",
                    "size": 3849689341,
                    "md5": "f53b70c97f7e3478346cd1dc29d9a0cb",
                    "modificationDate": "2019-08-30T15:14:52Z",
                    "locations": [
                        {
                            "link": "https://sra-pub-src-2.s3.amazonaws.com/SRR10039008/f4.m.mscs.DMSO2.rna.merged.sorted.bam.1",
                            "service": "s3",
                            "region": "us-east-1"
                        }
                    ]
                },
                {
                    "object": "remote|SRR10039061",
                    "type": "bam/gzip",
                    "name": "f4.m.mscs.TBT2.meth.merged.sorted.uniq.bam",
                    "size": 1775387120,
                    "md5": "f0f47bc6629a0465a2256872bc5f03cb",
                    "modificationDate": "2019-08-30T15:16:10Z",
                    "locations": [
                        {
                            "link": "https://sra-pub-src-2.s3.amazonaws.com/SRR10039061/f4.m.mscs.TBT2.meth.merged.sorted.uniq.bam.1",
                            "service": "s3",
                            "region": "us-east-1"
                        }
                    ]
                },
                {
                    "object": "remote|SRR10039036",
                    "type": "bam/gzip",
                    "name": "f3.m.mscs.DMSO2.meth.merged.sorted.uniq.bam",
                    "size": 1581966751,
                    "md5": "e0d63f5317600772b7637bbe0897a883",
                    "modificationDate": "2019-08-30T15:16:34Z",
                    "locations": [
                        {
                            "link": "https://sra-pub-src-2.s3.amazonaws.com/SRR10039036/f3.m.mscs.DMSO2.meth.merged.sorted.uniq.bam.1",
                            "service": "s3",
                            "region": "us-east-1"
                        }
                    ]
                },
                {
                    "object": "remote|SRR10039016",
                    "type": "bam/gzip",
                    "name": "f4.m.mscs.TBT5.rna.merged.sorted.bam",
                    "size": 4174462775,
                    "md5": "61ebdfd7429611426f6580d0b79ea0d8",
                    "modificationDate": "2019-08-30T15:16:19Z",
                    "locations": [
                        {
                            "link": "https://sra-pub-src-2.s3.amazonaws.com/SRR10039016/f4.m.mscs.TBT5.rna.merged.sorted.bam.1",
                            "service": "s3",
                            "region": "us-east-1"
                        }
                    ]
                },
                {
                    "object": "remote|SRR10039060",
                    "type": "bam/gzip",
                    "name": "f4.m.mscs.TBT1.meth.merged.sorted.uniq.bam",
                    "size": 2159707413,
                    "md5": "efc2759d453f4a6e408b1c682b6b5a77",
                    "modificationDate": "2019-08-30T15:17:17Z",
                    "locations": [
                        {
                            "link": "https://sra-pub-src-2.s3.amazonaws.com/SRR10039060/f4.m.mscs.TBT1.meth.merged.sorted.uniq.bam.1",
                            "service": "s3",
                            "region": "us-east-1"
                        }
                    ]
                },
                {
                    "object": "remote|SRR10038997",
                    "type": "bam/gzip",
                    "name": "f4.f.mscs.DMSO1.rna.merged.sorted.bam",
                    "size": 4082450137,
                    "md5": "87d8918c44be3eb9d3dc8681e2d2887d",
                    "modificationDate": "2019-08-30T15:16:10Z",
                    "locations": [
                        {
                            "link": "https://sra-pub-src-2.s3.amazonaws.com/SRR10038997/f4.f.mscs.DMSO1.rna.merged.sorted.bam.1",
                            "service": "s3",
                            "region": "us-east-1"
                        }
                    ]
                },
                {
                    "object": "remote|SRR10039047",
                    "type": "bam/gzip",
                    "name": "f4.f.mscs.DMSO3.meth.merged.sorted.uniq.bam",
                    "size": 2176286317,
                    "md5": "281a9378a90bca80aab47711492a6510",
                    "modificationDate": "2019-08-30T15:17:31Z",
                    "locations": [
                        {
                            "link": "https://sra-pub-src-2.s3.amazonaws.com/SRR10039047/f4.f.mscs.DMSO3.meth.merged.sorted.uniq.bam.1",
                            "service": "s3",
                            "region": "us-east-1"
                        }
                    ]
                },
                {
                    "object": "remote|SRR10039050",
                    "type": "bam/gzip",
                    "name": "f4.f.mscs.TBT1.meth.merged.sorted.uniq.bam",
                    "size": 2342234590,
                    "md5": "84338c845e25851e8c9be97693b05b5d",
                    "modificationDate": "2019-08-30T15:17:30Z",
                    "locations": [
                        {
                            "link": "https://sra-pub-src-2.s3.amazonaws.com/SRR10039050/f4.f.mscs.TBT1.meth.merged.sorted.uniq.bam.1",
                            "service": "s3",
                            "region": "us-east-1"
                        }
                    ]
                },
                {
                    "object": "remote|SRR10039051",
                    "type": "bam/gzip",
                    "name": "f4.f.mscs.TBT2.meth.merged.sorted.uniq.bam",
                    "size": 2302165922,
                    "md5": "20ca90080cec6cb114138c0651962cc5",
                    "modificationDate": "2019-08-30T15:17:26Z",
                    "locations": [
                        {
                            "link": "https://sra-pub-src-2.s3.amazonaws.com/SRR10039051/f4.f.mscs.TBT2.meth.merged.sorted.uniq.bam.1",
                            "service": "s3",
                            "region": "us-east-1"
                        }
                    ]
                },
                {
                    "object": "remote|SRR10039040",
                    "type": "bam/gzip",
                    "name": "f3.m.mscs.TBT1.meth.merged.sorted.uniq.bam",
                    "size": 1635628983,
                    "md5": "396b5290143c03dc3a01a75e9a88f9ea",
                    "modificationDate": "2019-08-30T15:17:35Z",
                    "locations": [
                        {
                            "link": "https://sra-pub-src-2.s3.amazonaws.com/SRR10039040/f3.m.mscs.TBT1.meth.merged.sorted.uniq.bam.1",
                            "service": "s3",
                            "region": "us-east-1"
                        }
                    ]
                },
                {
                    "object": "remote|SRR10039044",
                    "type": "bam/gzip",
                    "name": "f3.m.mscs.TBT5.meth.merged.sorted.uniq.bam",
                    "size": 1538770084,
                    "md5": "b87d312e1a06dfea8091861d68e670a1",
                    "modificationDate": "2019-08-30T15:18:01Z",
                    "locations": [
                        {
                            "link": "https://sra-pub-src-2.s3.amazonaws.com/SRR10039044/f3.m.mscs.TBT5.meth.merged.sorted.uniq.bam.1",
                            "service": "s3",
                            "region": "us-east-1"
                        }
                    ]
                },
                {
                    "object": "remote|SRR10039035",
                    "type": "bam/gzip",
                    "name": "f3.m.mscs.DMSO1.meth.merged.sorted.uniq.bam",
                    "size": 1643327617,
                    "md5": "1c9fa73b04b5e64dd58b9808d028e7cf",
                    "modificationDate": "2019-08-30T15:17:52Z",
                    "locations": [
                        {
                            "link": "https://sra-pub-src-2.s3.amazonaws.com/SRR10039035/f3.m.mscs.DMSO1.meth.merged.sorted.uniq.bam.1",
                            "service": "s3",
                            "region": "us-east-1"
                        }
                    ]
                },
                {
                    "object": "remote|SRR10039043",
                    "type": "bam/gzip",
                    "name": "f3.m.mscs.TBT4.meth.merged.sorted.uniq.bam",
                    "size": 1641269802,
                    "md5": "da807efedd348ebb3b82d061d5d8ef35",
                    "modificationDate": "2019-08-30T15:17:35Z",
                    "locations": [
                        {
                            "link": "https://sra-pub-src-2.s3.amazonaws.com/SRR10039043/f3.m.mscs.TBT4.meth.merged.sorted.uniq.bam.1",
                            "service": "s3",
                            "region": "us-east-1"
                        }
                    ]
                },
                {
                    "object": "remote|SRR10039045",
                    "type": "bam/gzip",
                    "name": "f4.f.mscs.DMSO1.meth.merged.sorted.uniq.bam",
                    "size": 2409332283,
                    "md5": "e8e58038e7eb245f4d17bdd650e816ec",
                    "modificationDate": "2019-08-30T15:18:03Z",
                    "locations": [
                        {
                            "link": "https://sra-pub-src-2.s3.amazonaws.com/SRR10039045/f4.f.mscs.DMSO1.meth.merged.sorted.uniq.bam.1",
                            "service": "s3",
                            "region": "us-east-1"
                        }
                    ]
                },
                {
                    "object": "remote|SRR10039048",
                    "type": "bam/gzip",
                    "name": "f4.f.mscs.DMSO4.meth.merged.sorted.uniq.bam",
                    "size": 2012548608,
                    "md5": "b4b6c01eb796979c5f950354d02cfb03",
                    "modificationDate": "2019-08-30T15:17:55Z",
                    "locations": [
                        {
                            "link": "https://sra-pub-src-2.s3.amazonaws.com/SRR10039048/f4.f.mscs.DMSO4.meth.merged.sorted.uniq.bam.1",
                            "service": "s3",
                            "region": "us-east-1"
                        }
                    ]
                },
                {
                    "object": "remote|SRR10039063",
                    "type": "bam/gzip",
                    "name": "f4.m.mscs.TBT4.meth.merged.sorted.uniq.bam",
                    "size": 1953062144,
                    "md5": "cf3259e0a43e1fdf305119f6b81a34f8",
                    "modificationDate": "2019-08-30T15:18:39Z",
                    "locations": [
                        {
                            "link": "https://sra-pub-src-2.s3.amazonaws.com/SRR10039063/f4.m.mscs.TBT4.meth.merged.sorted.uniq.bam.1",
                            "service": "s3",
                            "region": "us-east-1"
                        }
                    ]
                },
                {
                    "object": "remote|SRR10039022",
                    "type": "bam/gzip",
                    "name": "f4.m.liv.TBT2.rna.merged.sorted.bam",
                    "size": 1508577124,
                    "md5": "31e34de4ac435d831dccef596ab8f920",
                    "modificationDate": "2019-08-30T15:18:40Z",
                    "locations": [
                        {
                            "link": "https://sra-pub-src-2.s3.amazonaws.com/SRR10039022/f4.m.liv.TBT2.rna.merged.sorted.bam.1",
                            "service": "s3",
                            "region": "us-east-1"
                        }
                    ]
                },
                {
                    "object": "remote|SRR10039056",
                    "type": "bam/gzip",
                    "name": "f4.m.mscs.DMSO2.meth.merged.sorted.uniq.bam",
                    "size": 2177946433,
                    "md5": "78a6d739aa05d0d438a60b610134eb80",
                    "modificationDate": "2019-08-30T15:19:36Z",
                    "locations": [
                        {
                            "link": "https://sra-pub-src-2.s3.amazonaws.com/SRR10039056/f4.m.mscs.DMSO2.meth.merged.sorted.uniq.bam.1",
                            "service": "s3",
                            "region": "us-east-1"
                        }
                    ]
                },
                {
                    "object": "remote|SRR10039053",
                    "type": "bam/gzip",
                    "name": "f4.f.mscs.TBT4.meth.merged.sorted.uniq.bam",
                    "size": 2341211970,
                    "md5": "03c03029ac492b35c150f30be05da2b6",
                    "modificationDate": "2019-08-30T15:20:36Z",
                    "locations": [
                        {
                            "link": "https://sra-pub-src-2.s3.amazonaws.com/SRR10039053/f4.f.mscs.TBT4.meth.merged.sorted.uniq.bam.1",
                            "service": "s3",
                            "region": "us-east-1"
                        }
                    ]
                },
                {
                    "object": "remote|SRR10039052",
                    "type": "bam/gzip",
                    "name": "f4.f.mscs.TBT3.meth.merged.sorted.uniq.bam",
                    "size": 2001635807,
                    "md5": "8693d3febec2da8af2c8bba896347f66",
                    "modificationDate": "2019-08-30T15:20:04Z",
                    "locations": [
                        {
                            "link": "https://sra-pub-src-2.s3.amazonaws.com/SRR10039052/f4.f.mscs.TBT3.meth.merged.sorted.uniq.bam.1",
                            "service": "s3",
                            "region": "us-east-1"
                        }
                    ]
                },
                {
                    "object": "remote|SRR10039062",
                    "type": "bam/gzip",
                    "name": "f4.m.mscs.TBT3.meth.merged.sorted.uniq.bam",
                    "size": 2220289023,
                    "md5": "924d1799400fd1b362dc50d3f263c0f9",
                    "modificationDate": "2019-08-30T15:20:46Z",
                    "locations": [
                        {
                            "link": "https://sra-pub-src-2.s3.amazonaws.com/SRR10039062/f4.m.mscs.TBT3.meth.merged.sorted.uniq.bam.1",
                            "service": "s3",
                            "region": "us-east-1"
                        }
                    ]
                },
                {
                    "object": "remote|SRR10039058",
                    "type": "bam/gzip",
                    "name": "f4.m.mscs.DMSO4.meth.merged.sorted.uniq.bam",
                    "size": 1844082840,
                    "md5": "e1a3558753a96d427417288fe935560e",
                    "modificationDate": "2019-08-30T15:20:00Z",
                    "locations": [
                        {
                            "link": "https://sra-pub-src-2.s3.amazonaws.com/SRR10039058/f4.m.mscs.DMSO4.meth.merged.sorted.uniq.bam.1",
                            "service": "s3",
                            "region": "us-east-1"
                        }
                    ]
                },
                {
                    "object": "remote|SRR10039046",
                    "type": "bam/gzip",
                    "name": "f4.f.mscs.DMSO2.meth.merged.sorted.uniq.bam",
                    "size": 2413863049,
                    "md5": "098d7f0b60f941e0691b80ceff03f01f",
                    "modificationDate": "2019-08-30T15:21:05Z",
                    "locations": [
                        {
                            "link": "https://sra-pub-src-2.s3.amazonaws.com/SRR10039046/f4.f.mscs.DMSO2.meth.merged.sorted.uniq.bam.1",
                            "service": "s3",
                            "region": "us-east-1"
                        }
                    ]
                },
                {
                    "object": "remote|SRR10039055",
                    "type": "bam/gzip",
                    "name": "f4.m.mscs.DMSO1.meth.merged.sorted.uniq.bam",
                    "size": 2356406514,
                    "md5": "9205d3f14c5d4efbe3bdba46fc264665",
                    "modificationDate": "2019-08-30T15:21:09Z",
                    "locations": [
                        {
                            "link": "https://sra-pub-src-2.s3.amazonaws.com/SRR10039055/f4.m.mscs.DMSO1.meth.merged.sorted.uniq.bam.1",
                            "service": "s3",
                            "region": "us-east-1"
                        }
                    ]
                },
                {
                    "object": "remote|SRR10039049",
                    "type": "bam/gzip",
                    "name": "f4.f.mscs.DMSO5.meth.merged.sorted.uniq.bam",
                    "size": 2299145289,
                    "md5": "aa8fbf47c010ee82e783f52f9e7a21d0",
                    "modificationDate": "2019-08-30T15:21:11Z",
                    "locations": [
                        {
                            "link": "https://sra-pub-src-2.s3.amazonaws.com/SRR10039049/f4.f.mscs.DMSO5.meth.merged.sorted.uniq.bam.1",
                            "service": "s3",
                            "region": "us-east-1"
                        }
                    ]
                },
                {
                    "object": "remote|SRR10039026",
                    "type": "bam/gzip",
                    "name": "f3.f.mscs.DMSO2.meth.merged.sorted.uniq.bam",
                    "size": 1161806552,
                    "md5": "f1eacfb0c319b5f0642f7793e6f4e864",
                    "modificationDate": "2019-08-30T15:24:31Z",
                    "locations": [
                        {
                            "link": "https://sra-pub-src-2.s3.amazonaws.com/SRR10039026/f3.f.mscs.DMSO2.meth.merged.sorted.uniq.bam.1",
                            "service": "s3",
                            "region": "us-east-1"
                        }
                    ]
                },
                {
                    "object": "remote|SRR10039064",
                    "type": "bam/gzip",
                    "name": "f4.m.mscs.TBT5.meth.merged.sorted.uniq.bam",
                    "size": 2464420533,
                    "md5": "681a82ce611ab1da03ba6b9af0b5b76c",
                    "modificationDate": "2019-08-30T15:24:37Z",
                    "locations": [
                        {
                            "link": "https://sra-pub-src-2.s3.amazonaws.com/SRR10039064/f4.m.mscs.TBT5.meth.merged.sorted.uniq.bam.1",
                            "service": "s3",
                            "region": "us-east-1"
                        }
                    ]
                },
                {
                    "object": "remote|SRR10039012",
                    "type": "bam/gzip",
                    "name": "f4.m.mscs.TBT1.rna.merged.sorted.bam",
                    "size": 5829617624,
                    "md5": "cc0b9902928b8f1717ba973110a1cb4c",
                    "modificationDate": "2019-08-30T15:24:37Z",
                    "locations": [
                        {
                            "link": "https://sra-pub-src-2.s3.amazonaws.com/SRR10039012/f4.m.mscs.TBT1.rna.merged.sorted.bam.1",
                            "service": "s3",
                            "region": "us-east-1"
                        }
                    ]
                },
                {
                    "object": "remote|SRR10039009",
                    "type": "bam/gzip",
                    "name": "f4.m.mscs.DMSO3.rna.merged.sorted.bam",
                    "size": 5943466097,
                    "md5": "0c1489b9bc711f659c8483cd85bf72ba",
                    "modificationDate": "2019-08-30T15:24:35Z",
                    "locations": [
                        {
                            "link": "https://sra-pub-src-2.s3.amazonaws.com/SRR10039009/f4.m.mscs.DMSO3.rna.merged.sorted.bam.1",
                            "service": "s3",
                            "region": "us-east-1"
                        }
                    ]
                },
                {
                    "object": "remote|SRR10039001",
                    "type": "bam/gzip",
                    "name": "f4.f.mscs.DMSO5.rna.merged.sorted.bam",
                    "size": 5697641677,
                    "md5": "5b415ddd910dae4155559996861667e3",
                    "modificationDate": "2019-08-30T15:25:43Z",
                    "locations": [
                        {
                            "link": "https://sra-pub-src-2.s3.amazonaws.com/SRR10039001/f4.f.mscs.DMSO5.rna.merged.sorted.bam.1",
                            "service": "s3",
                            "region": "us-east-1"
                        }
                    ]
                },
                {
                    "object": "remote|SRR10038998",
                    "type": "bam/gzip",
                    "name": "f4.f.mscs.DMSO2.rna.merged.sorted.bam",
                    "size": 6849877080,
                    "md5": "368ad164aae520e41e18c6649f2bb327",
                    "modificationDate": "2019-08-30T15:26:56Z",
                    "locations": [
                        {
                            "link": "https://sra-pub-src-2.s3.amazonaws.com/SRR10038998/f4.f.mscs.DMSO2.rna.merged.sorted.bam.1",
                            "service": "s3",
                            "region": "us-east-1"
                        }
                    ]
                },
                {
                    "object": "remote|SRR10039010",
                    "type": "bam/gzip",
                    "name": "f4.m.mscs.DMSO4.rna.merged.sorted.bam",
                    "size": 6074622123,
                    "md5": "bb7ce062c21cdb0f7c741a29a45fb230",
                    "modificationDate": "2019-08-30T15:26:27Z",
                    "locations": [
                        {
                            "link": "https://sra-pub-src-2.s3.amazonaws.com/SRR10039010/f4.m.mscs.DMSO4.rna.merged.sorted.bam.1",
                            "service": "s3",
                            "region": "us-east-1"
                        }
                    ]
                },
                {
                    "object": "remote|SRR10039003",
                    "type": "bam/gzip",
                    "name": "f4.f.mscs.TBT2.rna.merged.sorted.bam",
                    "size": 6883041891,
                    "md5": "d37fd1ba1a8a856226b435fccd91984f",
                    "modificationDate": "2019-08-30T15:26:07Z",
                    "locations": [
                        {
                            "link": "https://sra-pub-src-2.s3.amazonaws.com/SRR10039003/f4.f.mscs.TBT2.rna.merged.sorted.bam.1",
                            "service": "s3",
                            "region": "us-east-1"
                        }
                    ]
                },
                {
                    "object": "remote|SRR10039002",
                    "type": "bam/gzip",
                    "name": "f4.f.mscs.TBT1.rna.merged.sorted.bam",
                    "size": 6244261997,
                    "md5": "78ac0622450a3ce97aa22fe6af491667",
                    "modificationDate": "2019-08-30T15:25:55Z",
                    "locations": [
                        {
                            "link": "https://sra-pub-src-2.s3.amazonaws.com/SRR10039002/f4.f.mscs.TBT1.rna.merged.sorted.bam.1",
                            "service": "s3",
                            "region": "us-east-1"
                        }
                    ]
                },
                {
                    "object": "remote|SRR10039000",
                    "type": "bam/gzip",
                    "name": "f4.f.mscs.DMSO4.rna.merged.sorted.bam",
                    "size": 7897639356,
                    "md5": "ee97caf330941e2be32ad18fd3f18bc9",
                    "modificationDate": "2019-08-30T15:36:24Z",
                    "locations": [
                        {
                            "link": "https://sra-pub-src-2.s3.amazonaws.com/SRR10039000/f4.f.mscs.DMSO4.rna.merged.sorted.bam.1",
                            "service": "s3",
                            "region": "us-east-1"
                        }
                    ]
                },
                {
                    "object": "remote|SRR10039004",
                    "type": "bam/gzip",
                    "name": "f4.f.mscs.TBT3.rna.merged.sorted.bam",
                    "size": 7817556030,
                    "md5": "5587d88f19d46ce84e1e6f6848521f65",
                    "modificationDate": "2019-08-30T15:41:05Z",
                    "locations": [
                        {
                            "link": "https://sra-pub-src-2.s3.amazonaws.com/SRR10039004/f4.f.mscs.TBT3.rna.merged.sorted.bam.1",
                            "service": "s3",
                            "region": "us-east-1"
                        }
                    ]
                },
                {
                    "object": "remote|SRR10039013",
                    "type": "bam/gzip",
                    "name": "f4.m.mscs.TBT2.rna.merged.sorted.bam",
                    "size": 8215686966,
                    "md5": "8ac41503bb6c2784112da585c1eb2698",
                    "modificationDate": "2019-08-30T15:45:34Z",
                    "locations": [
                        {
                            "link": "https://sra-pub-src-2.s3.amazonaws.com/SRR10039013/f4.m.mscs.TBT2.rna.merged.sorted.bam.1",
                            "service": "s3",
                            "region": "us-east-1"
                        }
                    ]
                },
                {
                    "object": "remote|SRR10039014",
                    "type": "bam/gzip",
                    "name": "f4.m.mscs.TBT3.rna.merged.sorted.bam",
                    "size": 7900422617,
                    "md5": "29c57330ea177448fed8702e163906ac",
                    "modificationDate": "2019-08-30T16:20:46Z",
                    "locations": [
                        {
                            "link": "https://sra-pub-src-2.s3.amazonaws.com/SRR10039014/f4.m.mscs.TBT3.rna.merged.sorted.bam.1",
                            "service": "s3",
                            "region": "us-east-1"
                        }
                    ]
                },
                {
                    "object": "remote|SRR10039007",
                    "type": "bam/gzip",
                    "name": "f4.m.mscs.DMSO1.rna.merged.sorted.bam",
                    "size": 6065726559,
                    "md5": "eb82f46bfe6673b11aa92a588fef0c6d",
                    "modificationDate": "2019-09-10T00:57:15Z",
                    "locations": [
                        {
                            "link": "https://sra-pub-src-2.s3.amazonaws.com/SRR10039007/f4.m.mscs.DMSO1.rna.merged.sorted.bam.1",
                            "service": "s3",
                            "region": "us-east-1"
                        }
                    ]
                },
                {
                    "object": "remote|SRR10039011",
                    "type": "bam/gzip",
                    "name": "f4.m.mscs.DMSO5.rna.merged.sorted.bam",
                    "size": 8090940973,
                    "md5": "1dff01a535d96eba30a90d8951b9f4d1",
                    "modificationDate": "2019-09-10T01:30:09Z",
                    "locations": [
                        {
                            "link": "https://sra-pub-src-2.s3.amazonaws.com/SRR10039011/f4.m.mscs.DMSO5.rna.merged.sorted.bam.1",
                            "service": "s3",
                            "region": "us-east-1"
                        }
                    ]
                },
                {
                    "object": "remote|SRR10039015",
                    "type": "bam/gzip",
                    "name": "f4.m.mscs.TBT4.rna.merged.sorted.bam",
                    "size": 8416652746,
                    "md5": "6246b9422cfa07f8aaccdf3b07c81fa8",
                    "modificationDate": "2019-09-10T01:37:50Z",
                    "locations": [
                        {
                            "link": "https://sra-pub-src-2.s3.amazonaws.com/SRR10039015/f4.m.mscs.TBT4.rna.merged.sorted.bam.1",
                            "service": "s3",
                            "region": "us-east-1"
                        }
                    ]
                },
                {
                    "object": "remote|SRR10038999",
                    "type": "bam/gzip",
                    "name": "f4.f.mscs.DMSO3.rna.merged.sorted.bam",
                    "size": 7784420153,
                    "md5": "bc165489367092fae971adb8e84cb8a9",
                    "modificationDate": "2019-09-10T01:39:31Z",
                    "locations": [
                        {
                            "link": "https://sra-pub-src-2.s3.amazonaws.com/SRR10038999/f4.f.mscs.DMSO3.rna.merged.sorted.bam.1",
                            "service": "s3",
                            "region": "us-east-1"
                        }
                    ]
                }
            ]
        }
    ]
}
"""
