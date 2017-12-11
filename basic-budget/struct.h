
// Bool
typedef enum {
	false,
	true
} bool;

// Cost entry
typedef struct cost_entry {
	int cost;
	int category;
	bool is_cost_valid;
	bool is_category_valid;
} cost_entry;

// Category structure
typedef struct category {
	int id;
	char name[MAX_CHARACTER_BUFFER];
	struct category *next;
} category;
