#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import psutil
import platform
from datetime import datetime
from typing import Dict, List, Tuple
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class SystemMonitor:
    """Sistem kaynaklarını izlemek için ana sınıf."""
    
    def __init__(self):
        self.system = platform.system()
        self.cpu_count = psutil.cpu_count()
        self.cpu_count_logical = psutil.cpu_count(logical=True)
    
    def get_cpu_info(self) -> Dict:
        """CPU kullanımı ve sıcaklık bilgilerini döndürür."""
        try:
            cpu_percent = psutil.cpu_percent(interval=1, percpu=True)
            cpu_freq = psutil.cpu_freq(percpu=True) if hasattr(psutil, 'cpu_freq') else None
            
            cpu_info = {
                'usage_per_cpu': cpu_percent,
                'average_usage': sum(cpu_percent) / len(cpu_percent),
                'frequency': cpu_freq,
                'physical_cores': self.cpu_count,
                'logical_cores': self.cpu_count_logical
            }
            
            # Sıcaklık bilgisi (platform desteği varsa)
            try:
                sensors = psutil.sensors_temperatures()
                if sensors:
                    cpu_info['temperature'] = sensors
            except AttributeError:
                cpu_info['temperature'] = None
                
            return cpu_info
            
        except Exception as e:
            logger.error(f"CPU bilgisi alınamadı: {str(e)}")
            return {}
    
    def get_memory_info(self) -> Dict:
        """Bellek kullanım bilgilerini döndürür."""
        try:
            virtual_mem = psutil.virtual_memory()
            swap = psutil.swap_memory()
            
            return {
                'total': virtual_mem.total,
                'available': virtual_mem.available,
                'used': virtual_mem.used,
                'free': virtual_mem.free,
                'percent': virtual_mem.percent,
                'swap_total': swap.total,
                'swap_used': swap.used,
                'swap_free': swap.free,
                'swap_percent': swap.percent
            }
            
        except Exception as e:
            logger.error(f"Bellek bilgisi alınamadı: {str(e)}")
            return {}
    
    def get_disk_info(self) -> List[Dict]:
        """Disk kullanım bilgilerini döndürür."""
        try:
            disks = []
            partitions = psutil.disk_partitions()
            
            for partition in partitions:
                try:
                    usage = psutil.disk_usage(partition.mountpoint)
                    disk_info = {
                        'device': partition.device,
                        'mountpoint': partition.mountpoint,
                        'fstype': partition.fstype,
                        'total': usage.total,
                        'used': usage.used,
                        'free': usage.free,
                        'percent': usage.percent
                    }
                    disks.append(disk_info)
                except PermissionError:
                    continue
                    
            return disks
            
        except Exception as e:
            logger.error(f"Disk bilgisi alınamadı: {str(e)}")
            return []
    
    def get_network_info(self) -> Dict:
        """Ağ kullanım bilgilerini döndürür."""
        try:
            net_io = psutil.net_io_counters()
            net_if = psutil.net_if_stats()
            
            return {
                'bytes_sent': net_io.bytes_sent,
                'bytes_recv': net_io.bytes_recv,
                'packets_sent': net_io.packets_sent,
                'packets_recv': net_io.packets_recv,
                'interfaces': {
                    iface: {
                        'isup': stats.isup,
                        'speed': stats.speed
                    } for iface, stats in net_if.items()
                }
            }
            
        except Exception as e:
            logger.error(f"Ağ bilgisi alınamadı: {str(e)}")
            return {}
    
    def get_top_processes(self, limit: int = 10) -> List[Dict]:
        """En çok kaynak tüketen süreçleri döndürür."""
        try:
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                try:
                    pinfo = proc.info
                    processes.append({
                        'pid': pinfo['pid'],
                        'name': pinfo['name'],
                        'cpu_percent': pinfo['cpu_percent'],
                        'memory_percent': pinfo['memory_percent']
                    })
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    continue
                    
            # CPU kullanımına göre sırala
            return sorted(processes, 
                        key=lambda x: x['cpu_percent'], 
                        reverse=True)[:limit]
                        
        except Exception as e:
            logger.error(f"Süreç bilgisi alınamadı: {str(e)}")
            return []
    
    def get_system_status(self) -> Dict:
        """Tüm sistem durumunu tek bir sözlükte toplar."""
        return {
            'timestamp': datetime.now().isoformat(),
            'cpu': self.get_cpu_info(),
            'memory': self.get_memory_info(),
            'disk': self.get_disk_info(),
            'network': self.get_network_info(),
            'top_processes': self.get_top_processes()
        }

if __name__ == '__main__':
    # Basit test kodu
    monitor = SystemMonitor()
    status = monitor.get_system_status()
    print("Sistem Durumu:")
    print(f"CPU Kullanımı: {status['cpu'].get('average_usage', 0):.1f}%")
    print(f"Bellek Kullanımı: {status['memory'].get('percent', 0):.1f}%")
    print("\nEn Çok Kaynak Tüketen Süreçler:")
    for proc in status['top_processes'][:5]:
        print(f"{proc['name']}: CPU {proc['cpu_percent']:.1f}%")