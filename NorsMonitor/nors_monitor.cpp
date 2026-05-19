// NorsMonitor - System Resource Monitor
// License: GPLv3
#include <QApplication>
#include <QMainWindow>
#include <QVBoxLayout>
#include <QLabel>
#include <QTimer>
#include <QProgressBar>
#include <QFile>
#include <QTextStream>
#include <QDebug>

class NorsMonitor : public QMainWindow {
    Q_OBJECT

public:
    NorsMonitor(QWidget *parent = nullptr) : QMainWindow(parent) {
        setWindowTitle("🦅 NorsMonitor");
        resize(400, 200);

        // Apply Nors Theme
        setStyleSheet("QMainWindow { background-color: #0A192F; color: #FFFFFF; }"
                      "QLabel { color: #B0C4DE; font-family: 'Inter'; font-size: 14px; }"
                      "QProgressBar { border: 1px solid #B0C4DE; border-radius: 5px; text-align: center; color: white; }"
                      "QProgressBar::chunk { background-color: #00B4D8; width: 20px; }");

        QWidget *centralWidget = new QWidget(this);
        QVBoxLayout *layout = new QVBoxLayout(centralWidget);

        QLabel *title = new QLabel("Nors System Monitor");
        title->setStyleSheet("color: #00B4D8; font-size: 18px; font-weight: bold;");
        title->setAlignment(Qt::AlignCenter);
        layout->addWidget(title);

        layout->addWidget(new QLabel("CPU Usage:"));
        cpuBar = new QProgressBar();
        cpuBar->setRange(0, 100);
        layout->addWidget(cpuBar);

        layout->addWidget(new QLabel("Memory Usage:"));
        memBar = new QProgressBar();
        memBar->setRange(0, 100);
        layout->addWidget(memBar);

        setCentralWidget(centralWidget);

        QTimer *timer = new QTimer(this);
        connect(timer, &QTimer::timeout, this, &NorsMonitor::updateStats);
        timer->start(1000); // Update every second
    }

private slots:
    void updateStats() {
        // Dummy CPU update (In a real app, parse /proc/stat)
        int dummyCpu = qrand() % 100;
        cpuBar->setValue(dummyCpu);

        // Parse /proc/meminfo for Memory
        QFile file("/proc/meminfo");
        if (file.open(QIODevice::ReadOnly | QIODevice::Text)) {
            QTextStream in(&file);
            QString line;
            long totalMem = 0, freeMem = 0, availableMem = 0;

            while (!in.atEnd()) {
                line = in.readLine();
                if (line.startsWith("MemTotal:")) {
                    totalMem = line.split(QRegExp("\\s+"))[1].toLong();
                } else if (line.startsWith("MemAvailable:")) {
                    availableMem = line.split(QRegExp("\\s+"))[1].toLong();
                }
            }
            file.close();

            if (totalMem > 0) {
                int memPercent = 100 - (availableMem * 100 / totalMem);
                memBar->setValue(memPercent);
            }
        }
    }

private:
    QProgressBar *cpuBar;
    QProgressBar *memBar;
};

int main(int argc, char *argv[]) {
    QApplication app(argc, argv);
    NorsMonitor monitor;
    monitor.show();
    return app.exec();
}

#include "nors_monitor.moc"
