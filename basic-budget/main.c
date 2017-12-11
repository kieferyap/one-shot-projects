#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <stdlib.h>
#include <time.h>
#include <ctype.h>

#include "constants.h"
#include "struct.h"
#include "functions.h"

int main() {

	cost_entry *new_input;
	initialize_cost_entry(new_input);
	int new_category_id = 0;
	char buffer[MAX_CHARACTER_BUFFER];

	/*
	 * Cost input
	 */
	
	do {
		// Ask for the cost input
		printf(STR_INQUIRE_COST);

		// Check if input is a positive integer
		new_input->cost = input_unsigned_integer_guard();
		if (new_input->cost != -1) {
			new_input->is_cost_valid = true;
		}

		// Display error if otherwise
		else {
			printf(ERROR_INPUT);
		}

		// Continue asking for user input until the correct input has been given
	} while (new_input->is_cost_valid == false);

	/*
	 * Category input
	 */
	
	// Construct the category linked list
	FILE *category_read_file = open_file_for_reading(CATEGORY_FILENAME);
	category *categories, *current, *new;
	categories = (category *)malloc(sizeof(category));
	initialize_category(categories);

	if (category_read_file != NULL) {

		// Make way for the new category
		new = (category *)malloc(sizeof(category));

		while (fread(new, sizeof(category), 1, category_read_file) != 0) {
			new->next = NULL;

			// The very first category to be read
			if (categories->id == -1) {
				categories = new;
				current = categories;
			}

			// The next categories
			else {
				current->next = (category *)malloc(sizeof(category));
				current->next = new;
				current = current->next;

				if (feof(category_read_file)) {
					break;
				}
			}	

			// Allocate a new category for the next one
			new = (category *)malloc(sizeof(category));
		}

		free(new);
		fclose(category_read_file);
	}

	// Print the category linked list
	printf(STR_CATEGORY_DIVIDER);
	printf(STR_CATEGORY_HEADER);
	printf(STR_CATEGORY_DIVIDER);
	printf(STR_CATEGORY_ENTRY, 0, STR_NEW_CATEGORY);

	current = categories;

	// Traverse through the linked list
	if (current->id != -1) {
		while (true) {
			printf(STR_CATEGORY_ENTRY, current->id, current->name);

			// Break if we've reached the end
			if (current->next == NULL) {
				break;
			} 
			current = current->next;
		}
	}

	printf(STR_CATEGORY_DIVIDER);

	// Ask for user categories
	do {
		// Ask for the category input
		printf(STR_INQUIRE_CATEGORY);

		// Check if input is a positive integer, and is a valid category
		new_input->category = input_unsigned_integer_guard();

		// I wanted to make this more readable, but C kept on segfaulting without any logical reason... U:
		if ((new_input->category != -1 && current->id == -1 && new_input->category == 0) || (new_input->category != -1 && current->id != -1 && new_input->category <= current->id)) {
			new_input->is_category_valid = true;

			// Check if input is 0. If it is, then the user wants to add a new entry.
			if (new_input->category == 0) {
				FILE *category_write_file = fopen(CATEGORY_FILENAME, "a");
				new = (category *)malloc(sizeof(category));
				new->id = current->id == -1 ? 1 : current->id + 1;
				new->next = NULL;

				printf(STR_INQUIRE_NEW_CATEGORY);
				fflush(stdin);
				scanf("%[^\t\n]", &(new->name));

				// Save the new category to the binary file
				fwrite(new, sizeof(category), 1, category_write_file);

				if (current->id != -1) {
					current->next = new;
				}
				else {
					categories = new;
				}
			}
		}

		// Display error if otherwise
		else {
			printf(ERROR_INPUT);
		}

		// Continue asking for user input until the correct input has been given
	} while (new_input->is_category_valid == false);

	/*
	 * CSV Saving
	 */
	
	// Read expenses.csv as append
	FILE *expense_file = fopen(EXPENSES_FILENAME, "a");

	// Check the category name from the ID
	current = categories;
	if (current->id != -1) {
		while (true) {
			// Break if we've reached the chosen category ID, or the end.
			if (new_input->category == current->id || current->next == NULL) {
				break;
			} 
			current = current->next;
		}
	}

	// Get the current date/time
	time_t local_time = time(NULL);
	struct tm *time_structure = localtime(&local_time);
	char time_string[MAX_CHARACTER_BUFFER];
	strftime(time_string, sizeof(time_string), "%c", time_structure);

	// Append the new record
	fprintf(expense_file, STR_EXPENSE_ENTRY, time_string, new_input->cost, current->name);

	// Exit message
	char enter = ' ';
	printf(STR_STATUS_MESSAGE, time_string, new_input->cost, current->name);
	printf(STR_EXIT_MESSAGE);
	fflush(stdin);
	getchar(); 

	return 0;
}
