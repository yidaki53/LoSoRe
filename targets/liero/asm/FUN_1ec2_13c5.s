; FUN_1ec2_13c5  entry=1ec2:13c5 size=14
1ec2:13c5  MOV DX,0x3da
1ec2:13c8  IN AL,DX
1ec2:13c9  AND AL,0x8
1ec2:13cb  JNZ 0x1000:ffe8
1ec2:13cd  IN AL,DX
1ec2:13ce  AND AL,0x8
1ec2:13d0  JZ 0x1000:ffed
1ec2:13d2  RETF
