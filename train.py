import os
from pprint import pprint
from configs.config import parser
from dataset.data_module import DataModule
from lightning_tools.callbacks import add_callbacks
from models.HC_LLM import HC_LLM
from lightning.pytorch import seed_everything
from transformers import LlamaForCausalLM, LlamaTokenizer, AutoTokenizer,AutoModelForCausalLM
import lightning.pytorch as pl
import os
from lightning.pytorch.strategies import DDPStrategy
os.environ["TOKENIZERS_PARALLELISM"] = "false"  #or "true"

def train(args):

    dm = DataModule(args)
    callbacks = add_callbacks(args)
    trainer = pl.Trainer(
        devices=args.devices,
        num_nodes=args.num_nodes,
        strategy='ddp_find_unused_parameters_true',
        accelerator=args.accelerator,
        precision=args.precision,
        val_check_interval = args.val_check_interval,
        limit_val_batches = args.limit_val_batches,
        max_epochs = args.max_epochs,
        num_sanity_val_steps = args.num_sanity_val_steps,
        accumulate_grad_batches=args.accumulate_grad_batches,
        callbacks=callbacks["callbacks"], 
        logger=callbacks["loggers"]
    )

    if args.ckpt_file is not None:
        model = R2GenGPT.load_from_checkpoint(args.ckpt_file, strict=False)
    else:
        model = R2GenGPT(args)

    if args.test:
        trainer.test(model, datamodule=dm)
    elif args.validate:
        trainer.validate(model, datamodule=dm)
    else:
        trainer.fit(model, datamodule=dm)

def main():
    args = parser.parse_args()
    os.makedirs(args.savedmodel_path, exist_ok=True)
    pprint(vars(args))
    seed_everything(42, workers=True)

    train(args)


if __name__ == '__main__':
    main()
