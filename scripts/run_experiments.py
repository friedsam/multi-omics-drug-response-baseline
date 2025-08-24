
import yaml, argparse
from pathlib import Path
from src.pipeline.train import train_one_run

def main(cfg_path: str, run_id: str|None):
    doc = yaml.safe_load(Path(cfg_path).read_text())
    runs = doc["runs"]
    if run_id:
        runs = [r for r in runs if r["id"] == run_id]
        if not runs: raise SystemExit(f"No run with id={run_id}")
    for r in runs:
        print(f"[run] {r['id']}")
        res = train_one_run(r)
        print(f"  -> {res['metric_name']}: {res['metric']:.4f}")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--cfg", default="configs/experiments.yaml")
    ap.add_argument("--id", default=None)
    args = ap.parse_args()
    main(args.cfg, args.id)