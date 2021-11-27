#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>

typedef char (*fn_t)();

// The program is a PIE so we don't know at which address
// it loads, we'll use /proc/self/maps to find where.
static unsigned long pie_base_address(void) {
        FILE *maps = fopen("/proc/self/maps", "r");

        while (1) {
                unsigned long from;
                int pgoff;
                char *lib;

                fscanf(maps, "%lx-%*lx %*4c %x %*x:%*x %*lu %ms", &from, &pgoff, &lib);
                bool check = strstr(lib, "vault") && pgoff == 0;

                free(lib);
                if (check) {
                        return from;
                }
        }

        abort();
}

// This function runs when the process start, before main.
void __attribute__ ((constructor)) crack(void) {
	void *base_address = (void*)pie_base_address();

	void ***array = base_address + 0x017880;
	char *string = base_address + 0x00e090;

	for (int i = 0; i < 0x19; i++) {
		fn_t function = *array[string[i]];

		// Through trial and error we found that the function at these indexes are
		// in reality pointer to the another pointer, so we dereference them.
		//
		// We could do a better job by looking in more depth at the vtable but
		// it works just fine.
		if (i == 3 || i == 5 || i == 10 || i == 11 || i == 13 || i == 15 || i == 16 || i == 17 || i == 18 || i == 20 || i == 21 || i == 22 || i == 23) {
			function = *(fn_t*)function;
		}

		putchar(function());
	}

	putchar('\n');

	exit(0);
}
