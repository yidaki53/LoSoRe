```c
void FUN_24dd_3711(void) {
    uint16_t local_6;
    uint16_t local_4;
    uint16_t local_2;

    local_6 = *(uint16_t *)(BP + 0x6);
    if (*(uint16_t *)(ES + local_6 + 0x2) == 0xd7b1) {
        goto LAB_2000_8509;
    }
    if (*(uint16_t *)(ES + local_6 + 0x2) == 0xd7b2) {
        goto LAB_2000_8501;
    }
    *(uint16_t *)0x6410 = 0x67;
    goto LAB_2000_8519;

LAB_2000_8519:
    return;

LAB_2000_8509:
    // Code for LAB_2000_8509
    return;

LAB_2000_8501:
    // Code for LAB_2000_8501
    return;
}
```