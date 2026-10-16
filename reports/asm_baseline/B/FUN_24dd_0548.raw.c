```c
void FUN_24dd_0548(uint8_t AL) {
    uint16_t SI, DI;

    CALL_7d9d();
    SI = 0x2e94;
    DI = 0x2f14;
    if (AL != 0) {
        JMP_5331();
    } else {
        *(uint16_t *)0x640e = 0xe6;
        SI = 0x2644;
        DI = 0x2314;
        JMP_7e24();
    }
}
```