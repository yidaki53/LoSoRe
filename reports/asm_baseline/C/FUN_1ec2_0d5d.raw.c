```c
void __stdcall16far FUN_1ec2_0d5d(unsigned char param_1, int param_2, unsigned int param_3, unsigned char *param_4) {
    unsigned char *puVar1;
    unsigned int uVar2;
    unsigned char *puVar3;

    puVar3 = param_4;
    uVar2 = param_3;
    do {
        for (uVar2 = uVar2 | param_3; uVar2 != 0; uVar2 = uVar2 - 1) {
            puVar1 = puVar3;
            puVar3 = puVar3 + 1;
            *puVar1 = param_1;
        }
        puVar3 = puVar3 + (0x140 - param_3);
        param_2 = param_2 + -1;
        uVar2 = 0;
    } while (param_2 != 0);
    return;
}
```