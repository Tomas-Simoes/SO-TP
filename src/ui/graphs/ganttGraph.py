from PyQt6.QtWidgets import QWidget, QVBoxLayout, QSizePolicy
from PyQt6.QtCore import pyqtSlot
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class GanttChartWidget(QWidget):
    def __init__(self, processes, parent=None):
        super().__init__(parent)
        self.processes = processes

        # Remove o tamanho fixo para permitir melhor redimensionamento
        self.figure = Figure(dpi=100)
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setSizePolicy(QSizePolicy.Policy.Expanding,
                                 QSizePolicy.Policy.Expanding)
        
        # Aumentando as margens para melhor visualização
        self.figure.subplots_adjust(left=0.15, right=0.95, bottom=0.15, top=0.9)
        
        self.axes = self.figure.add_subplot(111)
        self.axes.set_title("Gantt Chart of Processes")
        self.axes.set_xlabel("Time")
        self.axes.set_ylabel("Processes")
        self.axes.grid(True)

        layout = QVBoxLayout(self)
        layout.addWidget(self.canvas)
        
        # Configurando o widget para expandir adequadamente
        self.setMinimumSize(300, 200)
        
        # Primeira atualização
        self.draw_gantt()

    @pyqtSlot(list)
    def updateGantt(self, processes):
        self.processes = processes
        self.draw_gantt()
        
    def resizeEvent(self, event):
        # Redesenha o gráfico quando o widget é redimensionado
        super().resizeEvent(event)
        self.canvas.draw()

    def draw_gantt(self):
        if not self.processes:
            return
            
        self.axes.clear()
        self.axes.set_title("Gantt Chart of Processes")
        self.axes.set_xlabel("Time Units")
        self.axes.set_ylabel("Processes")
        self.axes.grid(True)

        # Calcular espaçamento vertical dinâmico baseado no número de processos
        chart_height = 100
        bar_height = min(8, chart_height / (len(self.processes) * 2))
        spacing = bar_height * 1.5
        y_positions = [i * spacing for i in range(len(self.processes))]

        # Desenhar barras para cada processo
        for proc, y in zip(self.processes, y_positions):
            name = str(proc.pid)
            start = proc.startTime if proc.startTime is not None else 0
            duration = proc.burstTime if proc.burstTime > 0 else 0
            
            if duration > 0:
                self.axes.broken_barh(
                    [(start, duration)],
                    (y, bar_height),
                    facecolors=('tab:blue',)
                )
                
                # Ajustar o texto para garantir que esteja visível
                if duration > 2:  # Só adicionar texto se a barra for larga o suficiente
                    self.axes.text(
                        start + duration/2,
                        y + bar_height/2,
                        name,
                        ha='center', va='center', 
                        color='white',
                        fontsize=8
                    )

        # Ticks e limites
        self.axes.set_yticks([y + bar_height/2 for y in y_positions])
        self.axes.set_yticklabels([f"P{p.pid}" for p in self.processes])
        
        # Calcular limites do eixo X
        max_end = max((p.startTime or 0) + (p.burstTime or 0) for p in self.processes)
        self.axes.set_xlim(0, max_end * 1.05)  # Adicionar 5% de espaço
        
        # Calcular limites do eixo Y
        if y_positions:
            self.axes.set_ylim(0, y_positions[-1] + bar_height * 2)
        else:
            self.axes.set_ylim(0, bar_height * 2)

        # Ajustar o layout para aproveitar melhor o espaço
        self.figure.tight_layout()
        self.canvas.draw()