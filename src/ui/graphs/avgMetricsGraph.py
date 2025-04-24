# ui/graphs/metricsGraph.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QSizePolicy
from PyQt6.QtCore    import pyqtSlot
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure               import Figure
from clock import GlobalClock

class AvgMetricsGraph(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Holds (time, avg_turnaround, avg_waiting) samples
        self.data = []
        # Matplotlib figure & canvas
        self.fig = Figure(dpi=100)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setSizePolicy(QSizePolicy.Policy.Expanding,
                                  QSizePolicy.Policy.Expanding)
        # One subplot
        self.ax = self.fig.add_subplot(111)
        self.ax.set_title("Average Turnaround & Waiting Time")
        self.ax.set_xlabel("Time (s)")
        self.ax.set_ylabel("Time Units")
        self.ax.grid(True)
        # Two line objects, initialized empty
        self.line_turn, = self.ax.plot([], [], label="Avg Turnaround")
        self.line_wait, = self.ax.plot([], [], label="Avg Waiting")
        self.ax.legend()
        # Layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.canvas)

    @pyqtSlot(object)
    def updateAvgMetricsGraph(self, completed):
        """
        Slot that receives the current simulation time and a list of completed Process instances.
        Calculates average turnaround and waiting time, then redraws the graph.
        """
        # Calculate averages inside the widget
        if completed:
            avg_turnaround = sum(p.turnaroundTime for p in completed) / len(completed)
            avg_waiting    = sum(p.waitingTime    for p in completed) / len(completed)
        else:
            avg_turnaround = avg_waiting = 0.0

        # Append data and redraw
        self.data.append((GlobalClock.getTime(), avg_turnaround, avg_waiting))
        self._redraw()

    def _redraw(self):
        # unzip data
        times, turns, waits = zip(*self.data)
        # update lines
        self.line_turn.set_data(times, turns)
        self.line_wait.set_data(times, waits)
        # rescale axes
        self.ax.relim()
        self.ax.autoscale_view()
        self.canvas.draw()
