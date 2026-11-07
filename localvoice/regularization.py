"""Selective encoder freezing and training-only diagonal-Fisher EWC."""


def freeze_lower_encoder(model, count):
    if not isinstance(count, int) or isinstance(count, bool) or not 0 <= count <= len(model.model.encoder.layers):
        raise ValueError("freeze_encoder_layers must be an integer within the encoder depth")
    encoder = model.model.encoder
    if count:
        # Keep the shared acoustic front end fixed along with the lower blocks.
        encoder.conv1.requires_grad_(False)
        encoder.conv2.requires_grad_(False)
        for layer in encoder.layers[:count]:
            layer.requires_grad_(False)
    return {"frozen_lower_blocks": count, "encoder_depth": len(encoder.layers),
            "acoustic_front_end_frozen": bool(count),
            "frozen_encoder_parameters": sum(p.numel() for p in encoder.parameters() if not p.requires_grad)}


class FisherPenalty:
    def __init__(self, model, fisher):
        import torch
        parameters = dict(model.named_parameters())
        if not fisher or set(fisher) != {n for n, p in parameters.items() if p.requires_grad}:
            raise ValueError("Fisher tensors must match all trainable model parameters")
        if any(not torch.isfinite(f).all() or (f < 0).any() or f.shape != parameters[n].shape for n, f in fisher.items()):
            raise ValueError("Fisher tensors must have matching shapes, finite nonnegative values")
        total = sum(float(f.double().sum()) for f in fisher.values())
        if total <= 0:
            raise ValueError("Fisher must have positive trace")
        self.terms = [(p, p.detach().float().clone(), (fisher[n] / total).to(device=p.device, dtype=torch.float32))
                      for n, p in parameters.items() if n in fisher]
        self.trace_before_normalization = total

    def __call__(self):
        return sum((f * (p.float() - anchor).square()).sum() for p, anchor, f in self.terms)
