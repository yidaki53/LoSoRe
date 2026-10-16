```c
void __stdcall16far FUN_24dd_4905(unsigned char param_1, int param_2, unsigned char *param_3) {
    unsigned char *puVar1;
    unsigned char *puVar2;

    puVar2 = param_3;
    while (param_2 != 0) {
        puVar1 = puVar2;
        puVar2 = puVar2 + 1;
        *puVar1 = param_1;
        param_2 = param_2 - 1;
    }
    return;
}
```