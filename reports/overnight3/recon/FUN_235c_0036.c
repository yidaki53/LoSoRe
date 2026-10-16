/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_235c_0036
 * Generated: 2026-10-16 by distilled-Qwen2.5-Coder-1.5B (distilled-g3)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=- phi=- verdict=not-judged
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

#include <stdbool.h>

extern void out(undefined2, int);
extern void FUN_249c_01c3(int);
extern char FUN_235c_001a(void);

bool __cdecl16far FUN_235c_0036(void) {
    char cVar1;
    char local_4;

    out(*(undefined2 *)0x67d0, 1);
    FUN_249c_01c3(1);
    out(*(undefined2 *)0x67d0, 0);
    for (local_4 = 'd'; (cVar1 = FUN_235c_001a(), cVar1 != -0x56 && (local_4 != '\0'));
         local_4 = local_4 + -1) {
    }
    return local_4 != '\0';
}
