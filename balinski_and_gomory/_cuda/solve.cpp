#include <torch/extension.h>
#include "balinski-and-gomory-cuda/src/solver.h"
#include <tuple>

namespace py = pybind11;

// assume `solve` writes into X, U, V in-place
std::tuple<torch::Tensor, torch::Tensor, torch::Tensor>
solve_binding(torch::Tensor C, torch::Tensor X, torch::Tensor U, torch::Tensor V) {
    // basic checks (adjust as needed)
    TORCH_CHECK(C.dtype() == torch::kFloat32, "C must be float32");
    TORCH_CHECK(U.dtype() == torch::kFloat32, "U must be float32");
    TORCH_CHECK(V.dtype() == torch::kFloat32, "V must be float32");
    TORCH_CHECK(X.dtype() == torch::kInt32,   "X must be int32");

    // make sure memory layout matches your kernel's expectations
    auto Cc = C.contiguous();
    auto Xc = X.contiguous();
    auto Uc = U.contiguous();
    auto Vc = V.contiguous();

    int64_t n64 = Cc.size(0);
    TORCH_CHECK(n64 <= std::numeric_limits<int>::max(), "n too large");
    int n = static_cast<int>(n64);

    // call your CUDA solver (expects raw pointers)
    solve(Cc.data_ptr<float>(),
          Xc.data_ptr<int32_t>(),
          Uc.data_ptr<float>(),
          Vc.data_ptr<float>(),
          n);

    // return all three (or all four if you want C too)
    return std::make_tuple(Xc, Uc, Vc);
}

PYBIND11_MODULE(TORCH_EXTENSION_NAME, m) {
    m.def("solve", &solve_binding, "Custom CUDA solve");
}
