#include <iostream>
#include <dwg.h>

int main() {
    const char* filename = "your_dwg_file.dwg"; // Replace with your DWG file path

    // Open the DWG file
    dwg_t* dwg = dwg_read(filename, DWG_VERSION_2018);
    if (dwg == nullptr) {
        std::cerr << "Error: Could not open the DWG file." << std::endl;
        return 1;
    }

    // Check if the DWG file has blocks (example of accessing data)
    std::cout << "Number of blocks in the DWG file: " << dwg->header->num_blocks << std::endl;

    // Optionally, loop through and print block names
    for (int i = 0; i < dwg->header->num_blocks; ++i) {
        std::cout << "Block " << i << ": " << dwg->blocks[i]->name << std::endl;
    }

    // Close the DWG file
    dwg_close(dwg);

    return 0;
}