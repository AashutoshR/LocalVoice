import pytest


def test_distillation_masks_padding_and_never_backpropagates_into_teacher():
    torch = pytest.importorskip("torch")
    from localvoice.training import distillation_loss
    student = torch.tensor([[[2., 1., 0.], [9., -9., 0.]]], requires_grad=True)
    teacher = torch.tensor([[[0., 1., 2.], [-9., 9., 0.]]], requires_grad=True)
    labels = torch.tensor([[2, -100]])
    loss = distillation_loss(student, teacher, labels, 2.)
    assert loss.item() > 0
    loss.backward()
    assert teacher.grad is None
    assert student.grad[0, 0].abs().sum() > 0
    assert student.grad[0, 1].abs().sum() == 0
    assert distillation_loss(teacher.detach(), teacher, labels, 2.).item() == pytest.approx(0, abs=1e-6)
