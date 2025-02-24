#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from rich.console import Console
from rich.table import Table
from rich.live import Live
from rich.layout import Layout
from rich.panel import Panel
from rich import box
import time
from typing import Dict, List
import sys
sys.path.append('..')
from core.monitor import SystemMonitor

console = Console()

class MonitorCLI:
    """Sistem monitör için CLI arayüzü."""
    
    def __init__(self):
        self.monitor = SystemMonitor()
        self.console = Console()
        
    def _create_cpu_table(self, cpu_info: Dict) -> Table:
        """CPU bilgilerini tablo olarak formatlar."""
        table = Table(title="CPU Durumu", box=box.ROUNDED)
        table.add_column("Çekirdek", justify="right", style="cyan")
        table.add_column("Kullanım %", justify="right", style="green")
        table.add_column("Frekans", justify="right", style="magenta")
        
        for i, usage in enumerate(cpu_info.get('usage_per_cpu', [])):
            freq = cpu_info.get('frequency', [])
            freq_str = f"{freq[i].current:.1f}MHz" if freq and len(freq) > i else "N/A"
            table.add_row(
                f"CPU {i}",
                f"{usage:.1f}%",
                freq_str
            )
            
        return table
        
    def _create_memory_table(self, memory_info: Dict) -> Table:
        """Bellek bilgilerini tablo olarak formatlar."""
        table = Table(title="Bellek Durumu", box=box.ROUNDED)
        table.add_column("Tür", justify="right", style="cyan")
        table.add_column("Toplam", justify="right", style="green")
        table.add_column("Kullanılan", justify="right", style="yellow")
        table.add_column("Boş", justify="right", style="blue")
        table.add_column("Kullanım %", justify="right", style="red")
        
        def format_bytes(bytes_: int) -> str:
            for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
                if bytes_ < 1024:
                    return f"{bytes_:.1f}{unit}"
                bytes_ /= 1024
            return f"{bytes_:.1f}TB"
        
        table.add_row(
            "RAM",
            format_bytes(memory_info.get('total', 0)),
            format_bytes(memory_info.get('used', 0)),
            format_bytes(memory_info.get('free', 0)),
            f"{memory_info.get('percent', 0):.1f}%"
        )
        
        table.add_row(
            "Swap",
            format_bytes(memory_info.get('swap_total', 0)),
            format_bytes(memory_info.get('swap_used', 0)),
            format_bytes(memory_info.get('swap_free', 0)),
            f"{memory_info.get('swap_percent', 0):.1f}%"
        )
        
        return table
        
    def _create_process_table(self, processes: List[Dict]) -> Table:
        """Süreç bilgilerini tablo olarak formatlar."""
        table = Table(title="En Çok Kaynak Tüketen Süreçler", box=box.ROUNDED)
        table.add_column("PID", justify="right", style="cyan")
        table.add_column("İsim", style="green")
        table.add_column("CPU %", justify="right", style="yellow")
        table.add_column("Bellek %", justify="right", style="red")
        
        for proc in processes:
            table.add_row(
                str(proc['pid']),
                proc['name'],
                f"{proc['cpu_percent']:.1f}%",
                f"{proc['memory_percent']:.1f}%"
            )
            
        return table
        
    def _create_disk_table(self, disk_info: List[Dict]) -> Table:
        """Disk bilgilerini tablo olarak formatlar."""
        table = Table(title="Disk Durumu", box=box.ROUNDED)
        table.add_column("Sürücü", style="cyan")
        table.add_column("Toplam", justify="right", style="green")
        table.add_column("Kullanılan", justify="right", style="yellow")
        table.add_column("Boş", justify="right", style="blue")
        table.add_column("Kullanım %", justify="right", style="red")
        
        def format_bytes(bytes_: int) -> str:
            for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
                if bytes_ < 1024:
                    return f"{bytes_:.1f}{unit}"
                bytes_ /= 1024
            return f"{bytes_:.1f}TB"
        
        for disk in disk_info:
            table.add_row(
                disk['mountpoint'],
                format_bytes(disk['total']),
                format_bytes(disk['used']),
                format_bytes(disk['free']),
                f"{disk['percent']:.1f}%"
            )
            
        return table
        
    def _create_network_table(self, network_info: Dict) -> Table:
        """Ağ bilgilerini tablo olarak formatlar."""
        table = Table(title="Ağ Durumu", box=box.ROUNDED)
        table.add_column("Metrik", style="cyan")
        table.add_column("Değer", justify="right", style="green")
        
        def format_bytes(bytes_: int) -> str:
            for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
                if bytes_ < 1024:
                    return f"{bytes_:.1f}{unit}"
                bytes_ /= 1024
            return f"{bytes_:.1f}TB"
        
        table.add_row("Gönderilen", format_bytes(network_info.get('bytes_sent', 0)))
        table.add_row("Alınan", format_bytes(network_info.get('bytes_recv', 0)))
        table.add_row("Gönderilen Paket", str(network_info.get('packets_sent', 0)))
        table.add_row("Alınan Paket", str(network_info.get('packets_recv', 0)))
        
        return table
    
    def display_live_stats(self, refresh_rate: float = 2.0):
        """Canlı sistem istatistiklerini gösterir."""
        layout = Layout()
        layout.split_column(
            Layout(name="upper"),
            Layout(name="lower")
        )
        layout["upper"].split_row(
            Layout(name="cpu"),
            Layout(name="memory")
        )
        layout["lower"].split_row(
            Layout(name="processes"),
            Layout(name="disk"),
            Layout(name="network")
        )
        
        with Live(layout, refresh_per_second=1/refresh_rate) as live:
            try:
                while True:
                    status = self.monitor.get_system_status()
                    
                    layout["cpu"].update(self._create_cpu_table(status['cpu']))
                    layout["memory"].update(self._create_memory_table(status['memory']))
                    layout["processes"].update(self._create_process_table(status['top_processes']))
                    layout["disk"].update(self._create_disk_table(status['disk']))
                    layout["network"].update(self._create_network_table(status['network']))
                    
                    time.sleep(refresh_rate)
            except KeyboardInterrupt:
                console.print("\n[yellow]İzleme sonlandırıldı.[/yellow]")

def main():
    cli = MonitorCLI()
    console.print("[green]Sistem İzleme Başlatılıyor...[/green]")
    cli.display_live_stats()

if __name__ == '__main__':
    main()