
void __cdecl16near FUN_1000_2426(void)

{
  uint uVar1;
  char cVar2;
  undefined2 unaff_DS;
  
  FUN_42b5_04df();
  uVar1 = *(uint *)0x3ac;
  if (uVar1 != 0) {
    if (((int)uVar1 < 1) || (3 < (int)uVar1)) {
      if ((uVar1 == 4) || (uVar1 == 5)) {
        if ((((*(int *)0x3b0 < 0x12) &&
             ((cVar2 = FUN_1000_10fa(*(undefined2 *)0x3b0,*(int *)0x3ae + 1), cVar2 == '\0' &&
              (cVar2 = FUN_1000_10fa(*(undefined2 *)0x3b0,*(int *)0x3ae + 2), cVar2 == '\0')))) &&
            (cVar2 = FUN_1000_11b0(), cVar2 == '\0')) && (*(int *)0x3ac != 0)) {
          FUN_3de3_0b67(*(int *)0x3b0 + 1,*(undefined2 *)0x3ae);
          FUN_3de3_002d(0x23ed,0x3de3);
          *(int *)0x3ae = *(int *)0x3ae + 1;
          FUN_3de3_0bea(0x23fc,0x3de3,*(int *)0x3b0 + 1,*(undefined2 *)0x3ae);
          FUN_1000_1619(5);
          *(int *)0x3ac = *(int *)0x3ac + 1;
        }
        else {
          *(undefined2 *)0x3ac = 0;
          FUN_3de3_0b67(*(int *)0x3b0 + 1,*(undefined2 *)0x3ae);
          FUN_3de3_002d(0x23ed,0x3de3);
          FUN_3de3_0bea(0x240a,0x3de3,*(int *)0x3b0 + 1,*(undefined2 *)0x3ae);
          FUN_1000_1619(5);
        }
      }
      else if (((int)uVar1 < 6) || (0xf < (int)uVar1)) {
        if (((int)uVar1 < -3) || (uVar1 < 0x8000)) {
          if ((uVar1 == 0xfffb) || (uVar1 == 0xfffc)) {
            if (((*(int *)0x3b0 < 0x12) &&
                (((cVar2 = FUN_1000_10fa(*(undefined2 *)0x3b0,*(int *)0x3ae + -1), cVar2 == '\0' &&
                  (cVar2 = FUN_1000_10fa(*(undefined2 *)0x3b0,*(int *)0x3ae + -2), cVar2 == '\0'))
                 && (cVar2 = FUN_1000_11b0(), cVar2 == '\0')))) && (*(int *)0x3ac != 0)) {
              FUN_3de3_0b67(*(int *)0x3b0 + 1,*(undefined2 *)0x3ae);
              FUN_3de3_002d(0x23ed,0x3de3);
              *(int *)0x3ae = *(int *)0x3ae + -1;
              FUN_3de3_0bea(0x2419,0x3de3,*(int *)0x3b0 + 1,*(undefined2 *)0x3ae);
              FUN_1000_1619(5);
              *(int *)0x3ac = *(int *)0x3ac + -1;
            }
            else {
              *(undefined2 *)0x3ac = 0;
              FUN_3de3_0b67(*(int *)0x3b0 + 1,*(undefined2 *)0x3ae);
              FUN_3de3_002d(0x23ed,0x3de3);
              FUN_3de3_0bea(0x240a,0x3de3,*(int *)0x3b0 + 1,*(undefined2 *)0x3ae);
              FUN_1000_1619(5);
            }
          }
          else if (((int)uVar1 < -0xf) || (-4 < (int)uVar1)) {
            *(undefined2 *)0x3ac = 0;
            FUN_3de3_0b67(*(int *)0x3b0 + 1,*(undefined2 *)0x3ae);
            FUN_3de3_002d(0x23ed,0x3de3);
            FUN_3de3_0bea(0x240a,0x3de3,*(int *)0x3b0 + 1,*(undefined2 *)0x3ae);
            FUN_1000_1619(5);
          }
          else if (((*(int *)0x3b0 < 0x12) &&
                   ((cVar2 = FUN_1000_10fa(*(int *)0x3b0 + 1,*(int *)0x3ae + -1), cVar2 == '\0' &&
                    (cVar2 = FUN_1000_10fa(*(int *)0x3b0 + 1,*(int *)0x3ae + -2), cVar2 == '\0'))))
                  && ((cVar2 = FUN_1000_11b0(), cVar2 == '\0' && (*(int *)0x3ac != 0)))) {
            FUN_3de3_0b67(*(int *)0x3b0 + 1,*(undefined2 *)0x3ae);
            FUN_3de3_002d(0x23ed,0x3de3);
            *(int *)0x3ae = *(int *)0x3ae + -1;
            *(int *)0x3b0 = *(int *)0x3b0 + 1;
            FUN_3de3_0bea(0x2419,0x3de3,*(int *)0x3b0 + 1,*(undefined2 *)0x3ae);
            FUN_1000_1619(5);
            *(int *)0x3ac = *(int *)0x3ac + -1;
          }
          else {
            *(undefined2 *)0x3ac = 0;
            FUN_3de3_0b67(*(int *)0x3b0 + 1,*(undefined2 *)0x3ae);
            FUN_3de3_002d(0x23ed,0x3de3);
            FUN_3de3_0bea(0x240a,0x3de3,*(int *)0x3b0 + 1,*(undefined2 *)0x3ae);
            FUN_1000_1619(5);
          }
        }
        else if (((*(int *)0x3b0 < 2) ||
                 ((cVar2 = FUN_1000_10fa(*(int *)0x3b0 + -1,*(int *)0x3ae + -1), cVar2 != '\0' ||
                  (cVar2 = FUN_1000_10fa(*(int *)0x3b0 + -1,*(int *)0x3ae + -2), cVar2 != '\0'))))
                || (*(int *)0x3ac == 0)) {
          *(undefined2 *)0x3ac = 0;
        }
        else {
          FUN_3de3_0b67(*(int *)0x3b0 + 1,*(undefined2 *)0x3ae);
          FUN_3de3_002d(0x23ed,0x3de3);
          *(int *)0x3ae = *(int *)0x3ae + -1;
          *(int *)0x3b0 = *(int *)0x3b0 + -1;
          FUN_3de3_0bea(0x2419,0x3de3,*(int *)0x3b0 + 1,*(undefined2 *)0x3ae);
          FUN_1000_1619(5);
          *(int *)0x3ac = *(int *)0x3ac + -1;
        }
      }
      else if ((*(int *)0x3b0 < 0x12) &&
              ((((cVar2 = FUN_1000_10fa(*(int *)0x3b0 + 1,*(int *)0x3ae + 1), cVar2 == '\0' &&
                 (cVar2 = FUN_1000_10fa(*(int *)0x3b0 + 1,*(int *)0x3ae + 2), cVar2 == '\0')) &&
                (cVar2 = FUN_1000_11b0(), cVar2 == '\0')) && (*(int *)0x3ac != 0)))) {
        FUN_3de3_0b67(*(int *)0x3b0 + 1,*(undefined2 *)0x3ae);
        FUN_3de3_002d(0x23ed,0x3de3);
        *(int *)0x3ae = *(int *)0x3ae + 1;
        *(int *)0x3b0 = *(int *)0x3b0 + 1;
        FUN_3de3_0bea(0x23fc,0x3de3,*(int *)0x3b0 + 1,*(undefined2 *)0x3ae);
        FUN_1000_1619(5);
        *(int *)0x3ac = *(int *)0x3ac + 1;
      }
      else {
        *(undefined2 *)0x3ac = 0;
        FUN_3de3_0b67(*(int *)0x3b0 + 1,*(undefined2 *)0x3ae);
        FUN_3de3_002d(0x23ed,0x3de3);
        FUN_3de3_0bea(0x240a,0x3de3,*(int *)0x3b0 + 1,*(undefined2 *)0x3ae);
        FUN_1000_1619(5);
      }
    }
    else if ((*(int *)0x3b0 < 2) ||
            (((cVar2 = FUN_1000_10fa(*(int *)0x3b0 + -1,*(int *)0x3ae + 1), cVar2 != '\0' ||
              (cVar2 = FUN_1000_10fa(*(int *)0x3b0 + -1,*(int *)0x3ae + 2), cVar2 != '\0')) ||
             (*(int *)0x3ac == 0)))) {
      *(undefined2 *)0x3ac = 0;
    }
    else {
      FUN_3de3_0b67(*(int *)0x3b0 + 1,*(undefined2 *)0x3ae);
      FUN_3de3_002d(0x23ed,0x3de3);
      *(int *)0x3ae = *(int *)0x3ae + 1;
      *(int *)0x3b0 = *(int *)0x3b0 + -1;
      FUN_3de3_0bea(0x23fc,0x3de3,*(int *)0x3b0 + 1,*(undefined2 *)0x3ae);
      FUN_1000_1619(5);
      *(int *)0x3ac = *(int *)0x3ac + 1;
    }
  }
  return;
}

