/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_24dd_4732
 * Generated: 2026-10-16 by phi4:14b (sumfirst)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=3 phi=3 verdict=contested
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

#include <stdint.h>
#include <stdbool.h>

uint16_t FUN_24dd_4732(const char *input, uint16_t length) {
    int32_t result = 0;
    uint32_t carry = 0;
    uint32_t temp;
    bool negative = false;
    const char *ptr = input;
    uint16_t remaining = length;

    if (remaining == 0) {
        goto end;
    }

    if (*ptr == '+') {
        ptr++;
        remaining--;
    } else if (*ptr == '-') {
        negative = true;
        ptr++;
        remaining--;
    }

    if (*ptr == '$') {
        ptr++;
        remaining--;
        while (remaining != 0) {
            if (*ptr >= '0' && *ptr <= '9') {
                temp = (uint32_t)(*ptr - '0');
            } else if (*ptr >= 'A' && *ptr <= 'F') {
                temp = (uint32_t)(*ptr - 'A' + 10);
            } else if (*ptr >= 'a' && *ptr <= 'f') {
                temp = (uint32_t)(*ptr - 'a' + 10);
            } else {
                goto end;
            }

            if ((carry & 0xF000) != 0) {
                goto end;
            }

            uint32_t prev_result = result;
            result = result * 16 + temp;
            carry = (carry << 1 | (uint32_t)(prev_result < 0)) << 1 | (uint32_t)(result < prev_result) + (uint32_t)(result < 0);

            ptr++;
            remaining--;
        }
    } else {
        while (remaining != 0) {
            if (*ptr >= '0' && *ptr <= '9') {
                temp = (uint32_t)(*ptr - '0');
            } else if (*ptr >= 'A' && *ptr <= 'F') {
                temp = (uint32_t)(*ptr - 'A' + 10);
            } else if (*ptr >= 'a' && *ptr <= 'f') {
                temp = (uint32_t)(*ptr - 'a' + 10);
            } else if (*ptr >= '0' && *ptr <= '9') {
                temp = (uint32_t)(*ptr - '0');
            } else {
                goto end;
            }

            bool shift_carry = false;
            for (int i = 0; i < 4; i++) {
                bool bit_carry = result < 0;
                result = result << 1;
                carry = (carry << 1 | (uint32_t)bit_carry) << 1 | (uint32_t)(result < 0);
                if (carry & 0x10000) {
                    goto end;
                }
                shift_carry |= bit_carry;
            }

            result = (result & 0xFF00) | (result >> 8) | temp;
            ptr++;
            remaining--;
        }
    }

    if (negative) {
        bool result_nonzero = result != 0;
        result = -result;
        carry = -(uint32_t)result_nonzero - carry;
    }

    if ((int32_t)carry < 0) {
        goto end;
    }

    if (result != 0 || carry != 0) {
        return (uint16_t)((carry << 8) | (result & 0xFF));
    }

end:
    return (uint16_t)((carry << 8) | (result & 0xFF));
}
