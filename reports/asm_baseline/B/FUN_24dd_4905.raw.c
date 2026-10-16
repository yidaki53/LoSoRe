```c
void FUN_24dd_4905(uint16_t param1, uint16_t param2, uint8_t param3) {
    uint16_t bx = param1;
    uint16_t cx = param2;
    uint8_t al = param3;
    uint16_t es_di = *(uint16_t *)(bx + 8);
    uint16_t es = es_di >> 16;
    uint16_t di = es_di & 0xFFFF;

    __asm__ volatile (
        "cld\n\t"
        "rep stosb\n\t"
        : "+D" (di), "+c" (cx)
        : "a" (al), "m" (es)
        : "memory"
    );

    __asm__ volatile (
        "retf $0x8\n\t"
    );
}
```