import numpy as np
from skimage import io, color, filters
from skimage.transform import resize
from skimage.feature import canny
from PIL import Image, ImageDraw, ImageFont


class NonogramCreator:
    """Class to create a Nonogram puzzle from an image using edge detection."""

    def __init__(self, img_path, puzzle_size=(25, 25)):
        """ Initialize NonogramCreator with an image path and puzzle size. """
        self.img_path = img_path
        self.puzzle_size = puzzle_size
        self.image = self.load_image()
        self.puzzle_grid = None

    def load_image(self):
        """ Load and convert the image to grayscale. """
        image = io.imread(self.img_path)
        # Convert RGB to grayscale if image is in color
        if len(image.shape) == 3:
            image = color.rgb2gray(image)
        return image

    def downsample_image(self):
        """
        Resize the grayscale image to match the specified puzzle size.
        """
        return resize(self.image, self.puzzle_size, anti_aliasing=True)

    def contour_based(self, padding=5):
        """
        Generate a binary grid representing edges (puzzle grid) using contour detection.

        """
        downsampled = self.downsample_image()
        # Apply padding around the downsampled image
        padded_image = np.pad(downsampled, pad_width=padding, mode='reflect')
        # Smooth the padded image to reduce noise before edge detection
        smoothed = filters.gaussian(padded_image, sigma=0.5)
        # Detect edges using the Canny edge detector
        edges = canny(smoothed, sigma=0.5)
        # Remove padding to restore original dimensions
        edges_cropped = edges[padding:-padding, padding:-padding]
        # Convert edges to integers for binary grid representation
        self.puzzle_grid = edges_cropped.astype(int)
        return self.puzzle_grid

    def generate_clues(self):
        """
        Generate row and column clues for the Nonogram puzzle.

        """
        # Generate clues by analyzing each row and column in the binary puzzle grid
        row_clues = [self.extract_clues(row) for row in self.puzzle_grid]
        col_clues = [self.extract_clues(col) for col in self.puzzle_grid.T]
        return row_clues, col_clues

    def extract_clues(self, line):
        """
        Extract consecutive filled cell counts in a line (row or column).

        """
        clues = []
        count = 0
        for cell in line:
            # Count consecutive filled cells
            if cell == 1:
                count += 1
            elif count > 0:
                clues.append(count)
                count = 0
        if count > 0:
            clues.append(count)
        return clues if clues else [0]

    def trim_grid(self):
        """
        Remove empty rows and columns from the puzzle grid for a cleaner output.
        """
        # Remove empty rows
        row_non_empty = np.any(self.puzzle_grid, axis=1)
        self.puzzle_grid = self.puzzle_grid[row_non_empty, :]
        # Remove empty columns
        col_non_empty = np.any(self.puzzle_grid, axis=0)
        self.puzzle_grid = self.puzzle_grid[:, col_non_empty]

    def save_clues_to_file(self, row_clues, col_clues, output_file):
        """
        Save row and column clues to a text file.
        
        """
        with open(output_file, 'w') as f:
            for row in row_clues:
                f.write(" ".join(map(str, row)) + "\n")
            f.write("\n")
            for col in col_clues:
                f.write(" ".join(map(str, col)) + "\n")

    def display_puzzle_with_clues(self, row_clues, col_clues, output_image_file):
        """
        Display and save the Nonogram puzzle with row and column clues.

        """
        num_rows = len(row_clues)
        num_cols = len(col_clues)
        max_row_clues = max(len(clues) for clues in row_clues)
        max_col_clues = max(len(clues) for clues in col_clues)
        cell_size = 20  # Size of each cell in pixels
        font_size = 14  # Font size for clues

        # Calculate overall image dimensions
        width = (max_row_clues + num_cols) * cell_size
        height = (max_col_clues + num_rows) * cell_size
        # Create a blank white image
        image = Image.new("RGB", (width, height), "white")
        draw = ImageDraw.Draw(image)

        # Load a font for drawing text
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except IOError:
            font = ImageFont.load_default()

        # Draw filled cells in the grid
        for i in range(num_rows):
            for j in range(num_cols):
                if self.puzzle_grid[i, j] == 1:  # Filled cell
                    x = max_row_clues * cell_size + j * cell_size
                    y = max_col_clues * cell_size + i * cell_size
                    draw.rectangle(
                        [x, y, x + cell_size, y + cell_size],
                        fill="black"
                    )

        # Draw grid lines
        for i in range(num_rows + 1):
            y = max_col_clues * cell_size + i * cell_size
            draw.line([(max_row_clues * cell_size, y), (width, y)], fill="black")
        for j in range(num_cols + 1):
            x = max_row_clues * cell_size + j * cell_size
            draw.line([(x, max_col_clues * cell_size), (x, height)], fill="black")

        # Draw row clues
        for i, clues in enumerate(row_clues):
            y = max_col_clues * cell_size + i * cell_size + cell_size / 2
            for k, clue in enumerate(reversed(clues)):
                x = (max_row_clues - k - 1) * cell_size + cell_size / 2
                draw.text((x, y), str(clue), fill="black", font=font, anchor="mm")

        # Draw column clues
        for j, clues in enumerate(col_clues):
            x = max_row_clues * cell_size + j * cell_size + cell_size / 2
            for k, clue in enumerate(reversed(clues)):
                y = (max_col_clues - k - 1) * cell_size + cell_size / 2
                draw.text((x, y), str(clue), fill="black", font=font, anchor="mm")

        # Save the generated image
        image.save(output_image_file)

    def create_puzzle(self, output_text_file, output_image_file):
        """
        Complete the process of creating a Nonogram puzzle from an image.

        """
        self.contour_based()  # Generate the edge-based puzzle grid
        self.trim_grid()  # Remove empty rows and columns
        row_clues, col_clues = self.generate_clues()  # Extract clues
        self.save_clues_to_file(row_clues, col_clues, output_text_file)  # Save clues to file
        self.display_puzzle_with_clues(row_clues, col_clues, output_image_file)  # Display puzzle

if __name__ == "__main__":
    # Request inputs from user
    img_path = input("Enter the path of the image file: ").strip()
    grid_width = int(input("Enter the width of the Nonogram grid: "))
    grid_height = int(input("Enter the height of the Nonogram grid: "))
    puzzle_size = (grid_height, grid_width)
    output_text_file = "nonogram_clues.txt"
    output_image_file = "nonogram_image_with_clues.jpg"
    # Initialize NonogramCreator with the provided image and puzzle size
    nonogram = NonogramCreator(img_path, puzzle_size=puzzle_size)
    # Generate puzzle and save outputs
    nonogram.create_puzzle(output_text_file,output_image_file)
    print(f"Nonogram created! Clues saved to {output_text_file}, image saved to {output_image_file}.")