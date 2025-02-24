#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import logging
from pathlib import Path
from ui.cli import MonitorCLI
from rich.logging import RichHandler

def setup_logging():
    """Loglama yapılandırmasını ayarlar."""
    log_dir = Path(__file__).parent / "logs"
    log_dir.mkdir(exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            RichHandler(rich_tracebacks=True),
            logging.FileHandler(log_dir / "system_monitor.log")
        ]
    )

def parse_arguments():
    """Komut satırı argümanlarını ayrıştırır."""
    parser = argparse.ArgumentParser(
        description="Sistem İzleme ve Optimizasyon Aracı"
    )
    parser.add_argument(
        "--refresh",
        type=float,
        default=2.0,
        help="Yenileme hızı (saniye)"
    )
    return parser.parse_args()

def main():
    """Uygulamanın ana giriş noktası."""
    args = parse_arguments()
    setup_logging()
    
    logger = logging.getLogger(__name__)
    logger.info("Sistem İzleme başlatılıyor...")
    
    try:
        cli = MonitorCLI()
        cli.display_live_stats(refresh_rate=args.refresh)
    except KeyboardInterrupt:
        logger.info("Uygulama kullanıcı tarafından sonlandırıldı.")
    except Exception as e:
        logger.error(f"Beklenmeyen hata: {str(e)}", exc_info=True)
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())