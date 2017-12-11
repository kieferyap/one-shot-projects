
// Returns -1 if the input was not a positive integer. 
// Returns actual value if otherwise.
int input_unsigned_integer_guard() {
	char line[MAX_CHARACTER_BUFFER];
	int input;

	fflush(stdin);
	fgets(line, sizeof line, stdin);

	bool is_input_correct = sscanf(line, "%d", &input);
	bool is_input_unsigned = input >= 0;

	if (!is_input_correct || !is_input_unsigned) {
		input = -1;
	}
	return input;
}

// Initializes the cost_entry structure
void initialize_cost_entry(cost_entry *in) {
	in->cost = 0;
	in->category = 0;
	in->is_cost_valid = false;
	in->is_category_valid = false;
}

// Initializes the category structure
void initialize_category(category *category) {
	category->id = -1;
	strcpy(category->name, UNDEFINED_CATEGORY);
}

FILE* open_file_for_reading(char *filename) {
	FILE *file;

	// File doesn't exist: create file
	if(access(filename, F_OK ) == -1) {
		file = fopen(filename, "ab+");
	}

	file = fopen(filename, "rb");
	return file;
}