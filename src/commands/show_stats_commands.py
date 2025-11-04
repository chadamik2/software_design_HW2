from src.commands.base_command import Command
from src.commands.stats import StatsRegistry


class ShowStatsCommand(Command):
    def __init__(self, stats: StatsRegistry): self.stats = stats

    @property
    def name(self) -> str: return "show_stats"

    def execute(self):
        print("Статистика сценариев:")
        for ts, name, dur in self.stats.all():
            print(f"{name}: {dur * 1000:.2f} ms")
