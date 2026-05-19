// NorsDefender - Host Intrusion Detection Daemon
// License: GPLv3
#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <thread>
#include <chrono>
#include <sys/inotify.h>
#include <unistd.h>
#include <limits.h>

#define MAX_EVENTS 1024
#define LEN_NAME 1024
#define EVENT_SIZE (sizeof(struct inotify_event))
#define BUF_LEN (MAX_EVENTS * (EVENT_SIZE + LEN_NAME))

void log_alert(const std::string& message) {
    std::ofstream log_file("/var/log/nors_defender.log", std::ios_base::app);
    if(log_file.is_open()) {
        time_t now = time(0);
        char* dt = ctime(&now);
        std::string time_str(dt);
        time_str.pop_back(); // remove newline
        log_file << "[" << time_str << "] [ALERT] " << message << std::endl;
        std::cout << "\033[1;31m[ALERT]\033[0m " << message << std::endl;
    }
}

void monitor_directory(const std::string& path) {
    int length, i = 0;
    int fd;
    int wd;
    char buffer[BUF_LEN];

    fd = inotify_init();
    if (fd < 0) {
        std::cerr << "inotify_init failed" << std::endl;
        return;
    }

    wd = inotify_add_watch(fd, path.c_str(), IN_MODIFY | IN_CREATE | IN_DELETE);
    std::cout << "[*] NorsDefender monitoring: " << path << std::endl;

    while (true) {
        length = read(fd, buffer, BUF_LEN);
        if (length < 0) {
            std::cerr << "read failed" << std::endl;
            break;
        }

        i = 0;
        while (i < length) {
            struct inotify_event *event = (struct inotify_event *) &buffer[i];
            if (event->len) {
                if (event->mask & IN_CREATE) {
                    log_alert("File created in " + path + ": " + event->name);
                } else if (event->mask & IN_DELETE) {
                    log_alert("File deleted in " + path + ": " + event->name);
                } else if (event->mask & IN_MODIFY) {
                    log_alert("File modified in " + path + ": " + event->name);
                }
            }
            i += EVENT_SIZE + event->len;
        }
    }
    inotify_rm_watch(fd, wd);
    close(fd);
}

void check_suspicious_processes() {
    std::vector<std::string> blacklisted_processes = {"crypto_miner", "nc -e", "bash -i"};
    while(true) {
        // Very basic process check heuristic
        system("ps aux > /tmp/nors_ps_dump");
        std::ifstream ps_file("/tmp/nors_ps_dump");
        std::string line;
        while(std::getline(ps_file, line)) {
            for(const auto& proc : blacklisted_processes) {
                if(line.find(proc) != std::string::npos) {
                    log_alert("Suspicious process detected: " + proc + " | " + line);
                }
            }
        }
        std::this_thread::sleep_for(std::chrono::seconds(10));
    }
}

int main() {
    std::cout << "🦅 Starting NorsDefender HIDS Daemon..." << std::endl;
    
    // Start directory monitoring in separate threads
    std::thread t1(monitor_directory, "/etc");
    std::thread t2(monitor_directory, "/bin");
    std::thread t3(monitor_directory, "/usr/bin");
    
    // Start process monitoring
    std::thread t4(check_suspicious_processes);

    t1.join();
    t2.join();
    t3.join();
    t4.join();

    return 0;
}
