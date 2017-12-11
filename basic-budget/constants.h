
// Application constants
#define MAX_CHARACTER_BUFFER 256
#define CATEGORY_FILENAME "categories.bin"
#define EXPENSES_FILENAME "expenses.csv"

// Wording constants
#define STR_INQUIRE_COST "How much was it in yen? (e.g.: 350)\n> Your input: \0"
#define STR_CATEGORY_HEADER " id\t| name\n\0"
#define STR_CATEGORY_DIVIDER "--------+------\n\0"
#define STR_CATEGORY_ENTRY " %d\t| %s\n\0"
#define STR_EXPENSE_ENTRY "%s,%d,%s\n"
#define STR_NEW_CATEGORY "New Category\0"
#define STR_INQUIRE_NEW_CATEGORY "> New Category Name: \0"
#define STR_INQUIRE_CATEGORY "Which Category ID? (e.g.: 0, 1, 2, ...)\n> Your input: \0"
#define STR_STATUS_MESSAGE "You have entered:\n> Time: \t\t%s\n> Cost: \t\t%d\n> Category: \t\t%s\n\0"
#define STR_EXIT_MESSAGE "Hit the [ENTER] key to exit the application.\0"
#define UNDEFINED_CATEGORY "Undefined Category\0"
#define ERROR_INPUT "Please input a positive and valid integer.\n\n\0"
