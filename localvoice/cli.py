import argparse
import json
from .core import ROOT, config, validate_manifest, EXPERIMENTS


def main():
    parser = argparse.ArgumentParser(description="LocalVoice research workbench")
    sub = parser.add_subparsers(dest="command", required=True)
    serve = sub.add_parser("serve")
    serve.add_argument("--port", type=int, default=8000)
    sub.add_parser("prepare", help="Download and convert the Spanish FLEURS dataset")
    validate = sub.add_parser("validate")
    validate.add_argument("--manifest", default=None)
    train = sub.add_parser("train")
    train.add_argument("experiment", choices=[e["id"] for e in EXPERIMENTS if e["strategy"] != "baseline"])
    train.add_argument("--config", default="configs/training.json")
    evaluate = sub.add_parser("evaluate")
    evaluate.add_argument("experiment", choices=[e["id"] for e in EXPERIMENTS])
    evaluate.add_argument("--split", choices=["validation", "test"], default="validation")
    evaluate.add_argument("--final-test", action="store_true", help="Explicitly unlock held-out test evaluation after choices are frozen")
    sub.add_parser("gradio")
    sub.add_parser("matrix", help="Run the baseline and all four fine-tuning experiments sequentially")
    sub.add_parser("report", help="Refresh measured comparisons in the README and results report")
    args = parser.parse_args()
    if args.command == "serve":
        import uvicorn
        uvicorn.run("localvoice.server:app", host="127.0.0.1", port=args.port)
    elif args.command == "validate":
        result = validate_manifest(args.manifest)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        if not result["valid"]:
            raise SystemExit(1)
    elif args.command == "prepare":
        from .prepare import prepare
        prepare()
    elif args.command == "train":
        from .training import train
        train(args.experiment, ROOT / args.config)
    elif args.command == "evaluate":
        if args.split == "test" and not args.final_test:
            parser.error("Test set is locked. Finalize choices first, then pass --final-test.")
        from .training import evaluate
        evaluate(args.experiment, args.split)
    elif args.command == "gradio":
        from .gradio_app import launch
        launch()
    elif args.command == "matrix":
        from .matrix import run_matrix
        run_matrix()
    elif args.command == "report":
        from .reporting import write_results
        write_results()


if __name__ == "__main__":
    main()
