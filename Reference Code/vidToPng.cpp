/*
The main goal of this repository is to simplify the process of data collection
We're going to start with opening mp4 files in C++
-> We might sidetrack into files as drone videos may not be in mp4 (We'll make a file convertor)
We will be using openCV for this project
We will open the file
(Once AI is setup we can also integrate this into our program)
We want a start and end time.
We can use this calcualte frames
We also want an intial position, end position and a width x length (of the piece of trash)
These width x length can change given time but for now we assume that the drone is at a steady height
Using the start and end time we can calculate how many frames are in between these two images

Now we can begin taking screenshots beginning at the initial position.
[Side note from now I'll be calling our center as C]
The distance from C,Start and C,End can be expressed as a vector <i,j> with C,start being the origin (we simply allign for it when taking screenshots)
Thus at the next frame we know that the width x height should be moved by <i/t, j/t> [starting at <0,0>]
Here t is a constant that encapsulates the FPS and the total time taken

Now all that is left to do is find a way to capture screenshots and write them to a repository
We will use OpenCV's ROI (region of interst) functionality
(This will be explained as we move along this file)


Of course to avoid overfitting/memorization all of the pieces of trash processed through this method
should be under the influence of some sort of change in enviornemnt (i.e wind, different lighting, rain, etc.)
*/
//Importing OpenCV and bits/stdc++.h (because I'm lazy :D)
//mac initally:
#include <bits/stdc++.h>
#include <opencv2/opencv.hpp>
#include <filesystem>
#include <unistd.h>

namespace fs = std::filesystem;

std::vector<std::string> videos;

// Function to get the current working directory
std::string GetCurrentPath() {
    char buffer[PATH_MAX];
    if (getcwd(buffer, sizeof(buffer)) != nullptr) {
        return std::string(buffer);
    } else {
        perror("getcwd error: ");
        return "";
    }
}

// Function to create a directory
void CreateDirectory(const std::string& dirName) {
    if (!fs::exists(dirName)) {
        if (fs::create_directory(dirName)) {
            std::cout << "Directory created successfully: " << dirName << std::endl;
        } else {
            std::cerr << "Failed to create directory: " << dirName << std::endl;
        }
    } else {
        std::cout << "Directory already exists: " << dirName << std::endl;
    }
}

// Function to check if a file is a valid video
bool ValidVideo(const std::string& path) {
    cv::VideoCapture cap(path);
    return cap.isOpened();
}

// Helper function to process each video
void ProcessVideo(const std::string& videoPath, const std::string& outputDir, int frameIndex, int frameEnd) {
    std::cout << "Processing video: " << videoPath << std::endl;

    cv::VideoCapture cap(videoPath);
    if (!cap.isOpened()) {
        std::cerr << "Failed to open video: " << videoPath << std::endl;
        return;
    }

    int fps = static_cast<int>(cap.get(cv::CAP_PROP_FPS));
    int frameCount = static_cast<int>(cap.get(cv::CAP_PROP_FRAME_COUNT));
    std::cout << "Video FPS: " << fps << ", Total Frames: " << frameCount << std::endl;

    cv::Mat frame;
    while (cap.read(frame) && frameIndex<frameEnd) {
        std::string frameFile = outputDir + "/frame_" + std::to_string(frameIndex) + ".png";
        cv::imwrite(frameFile, frame);
        frameIndex++;
    }

    std::cout << "Processing complete! Frames saved to: " << outputDir << std::endl;
}

// Main function
int main() {
    std::cout << "Hey, EccoDrones Member!" << std::endl;

    // Get current path and create a directory for video uploads
    std::string currentPath = GetCurrentPath();
    if (currentPath.empty()) {
        std::cerr << "Error: Failed to retrieve current directory." << std::endl;
        return 1;
    }

    std::string uploadDir = currentPath + "/Upload Videos Here";
    CreateDirectory(uploadDir);

    std::cout << "Place all the videos you want to process in the directory: " << uploadDir << std::endl;

    // Scan for videos in the upload directory
    for (const auto& entry : fs::directory_iterator(uploadDir)) {
        if (entry.is_regular_file() && ValidVideo(entry.path().string())) {
            videos.push_back(entry.path().string());
        }
    }

    if (videos.empty()) {
        std::cout << "No valid videos found in the directory: " << uploadDir << std::endl;
        return 0;
    }

    // Create output directory for frames
    std::string outputDir = currentPath + "/Processed Frames";
    CreateDirectory(outputDir);

    // Process each video
    for (const auto& video : videos) {
        std::string videoOutputDir = outputDir + "/" + fs::path(video).stem().string();
        CreateDirectory(videoOutputDir);
        int frameIndex, frameEnd;
        std::cout<<"We're currently doing the video at: "<<fs::path(video).stem().string()<<" Please enter the frame Start and frame end";
        std::cin>>frameIndex>>frameEnd;
        ProcessVideo(video, videoOutputDir, std::min(frameIndex, frameEnd), std::max(frameIndex, frameEnd));
    }

    std::cout << "All videos processed! Frames are in: " << outputDir << std::endl;

    return 0;
}


//To run on macos, run: g++ -std=c++17 -o main main.cpp $(pkg-config --cflags --libs opencv4)
//followed by: ./main