```c
void FUN_24dd_3ed3(void) {
    uint16_t bx = __builtin_return_address(0);
    uint16_t dx = __builtin_frame_address(0);
    uint16_t di = *(uint16_t *)(bx + 0xc);
    uint16_t si = *(uint16_t *)(bx + 0x8);
    uint8_t al = *(uint8_t *)si;
    uint8_t ah = 0;
    uint16_t cx = *(uint16_t *)(bx + 0x6);
    if (cx <= 0) {
        cx = 1;
        si += cx;
        al -= cx;
        if (al < 0) {
            al++;
        }
    }
    cx = *(uint16_t *)(bx + 0x4);
    if (cx < 0) {
        cx = 0;
        if (al <= cx) {
            al = cx;
        }
    }
    if (al == 0) {
        *(uint8_t *)di = 0;
        cx = 0;
    } else {
        __asm__ volatile ("rep movsb" : "+D"(di), "+S"(si), "+c"(cx) : : "memory");
    }
    dx = __builtin_frame_address(0);
    __asm__ volatile ("retf $0x8");
}
```