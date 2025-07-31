import csv
import os

class CSVHandler:
    """Handles CSV file operations."""
    @staticmethod
    def read(file):
        """Read data from a CSV file."""
        if not os.path.exists(file):
            with open(file, mode="w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([])  # Write an empty row to initialize the file
        with open(file, mode="r") as f:
            reader = csv.reader(f)
            return list(reader)

    @staticmethod
    def write(file, data):
        """Write data to a CSV file."""
        with open(file, mode="w", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(data)


class EntityManagement:
    """Base class for managing different entities."""
    def __init__(self, file, entity_type, fields):
        self.file = file
        self.entity_type = entity_type
        self.fields = fields
        self.data = []
        self.load_data()

    def load_data(self):
        """Load data from the CSV file."""
        self.data = CSVHandler.read(self.file)

    def save_data(self):
        """Save data to the CSV file."""
        CSVHandler.write(self.file, self.data)

    def add(self, item):
        """Add a new item."""
        if len(item) != len(self.fields):
            print(f"Error: {self.entity_type} requires the following fields: {', '.join(self.fields)}")
        else:
            self.data.append(item)
            print(f"{self.entity_type} added successfully.")

    def view(self):
        """View all items."""
        if not self.data:
            print(f"No {self.entity_type}s available.")
        else:
            print(f"\nList of {self.entity_type}s:")
            print(", ".join(self.fields))
            for idx, item in enumerate(self.data, start=1):
                print(f"{idx}. {', '.join(item)}")

    def delete(self, index):
        """Delete an item by index."""
        if 0 <= index < len(self.data):
            self.data.pop(index)
            print(f"{self.entity_type} deleted successfully.")
        else:
            print(f"Invalid index. {self.entity_type} not found.")

    def update(self, index, new_item):
        """Update an item by index."""
        if 0 <= index < len(self.data):
            if len(new_item) != len(self.fields):
                print(f"Error: {self.entity_type} requires the following fields: {', '.join(self.fields)}")
            else:
                self.data[index] = new_item
                print(f"{self.entity_type} updated successfully.")
        else:
            print(f"Invalid index. {self.entity_type} not found.")


class Timetable:
    """Handles timetable generation and display."""
    def __init__(self, classes, compensatory_classes):
        self.classes = classes
        self.compensatory_classes = compensatory_classes

    def generate(self):
        """Generate and display the timetable."""
        timetable_data = []
        print("\nGenerated Timetable:")
        print("Regular Classes:")
        for cls in self.classes.data:
            print(f"  {', '.join(cls)}")
            timetable_data.append(["Class", *cls])

        print("\nCompensatory Classes:")
        for comp_class in self.compensatory_classes.data:
            print(f"  {', '.join(comp_class)}")
            timetable_data.append(["Compensatory Class", *comp_class])

        # Save timetable to CSV
        self.save_to_csv(timetable_data)

    def save_to_csv(self, timetable_data):
        """Save the generated timetable to a CSV file."""
        file = "timetable.csv"
        with open(file, mode="w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Type", "Course Code", "Class Day", "Class Time"])
            writer.writerows(timetable_data)
        print(f"\nTimetable saved to {file}")


class UniversityTimetableSystem:
    """Main system for managing the university timetable."""
    def __init__(self):
        self.courses = EntityManagement("courses.csv", "Course", ["Course Code", "Course Name"])
        self.instructors = EntityManagement("instructors.csv", "Instructor", ["Instructor Name", "Course Code"])
        self.classes = EntityManagement("classes.csv", "Class", ["Course Code", "Class Day", "Class Time"])
        self.compensatory_classes = EntityManagement(
            "compensatory_classes.csv", "Compensatory Class", ["Course Code", "Class Day", "Class Time"]
        )

    def menu(self):
        """Main menu for the system."""
        while True:
            print("\nUniversity Timetable System")
            print("1. Manage Courses")
            print("2. Manage Instructors")
            print("3. Manage Classes")
            print("4. Manage Compensatory Classes")
            print("5. Generate Timetable")
            print("6. Exit")
            choice = input("Enter your choice: ")
            if choice == "1":
                self.manage_entity(self.courses)
            elif choice == "2":
                self.manage_entity(self.instructors)
            elif choice == "3":
                self.manage_entity(self.classes)
            elif choice == "4":
                self.manage_entity(self.compensatory_classes)
            elif choice == "5":
                self.generate_timetable()
            elif choice == "6":
                print("Thank you for using the system. Goodbye!")
                break
            else:
                print("Invalid choice, try again.")

    def manage_entity(self, entity_manager):
        """Generic management menu for any entity."""
        while True:
            print(f"\n{entity_manager.entity_type} Management")
            print("1. Add")
            print("2. View")
            print("3. Update")
            print("4. Delete")
            print("5. Exit")
            choice = input("Enter your choice: ")
            if choice == "1":
                item = input(f"Enter {entity_manager.entity_type} details (comma-separated: {', '.join(entity_manager.fields)}): ").split(",")
                entity_manager.add(item)
            elif choice == "2":
                entity_manager.view()
            elif choice == "3":
                entity_manager.view()
                index = int(input(f"Enter the index of the {entity_manager.entity_type} to update: ")) - 1
                new_item = input(f"Enter new details (comma-separated: {', '.join(entity_manager.fields)}): ").split(",")
                entity_manager.update(index, new_item)
            elif choice == "4":
                entity_manager.view()
                index = int(input(f"Enter the index of the {entity_manager.entity_type} to delete: ")) - 1
                entity_manager.delete(index)
            elif choice == "5":
                entity_manager.save_data()
                break
            else:
                print("Invalid choice, try again.")

    def generate_timetable(self):
        """Generate the timetable."""
        timetable = Timetable(self.classes, self.compensatory_classes)
        timetable.generate()


# Main execution
if __name__ == "__main__":
    timetable_system = UniversityTimetableSystem()
    timetable_system.menu()
