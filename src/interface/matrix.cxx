/*Copyright (c) 2011, Edgar Solomonik, all rights reserved.*/

#include "common.h"
namespace CTF_int{
  struct int2
  {
    int i[2];
    int2(int a, int b)
    {
      i[0] = a;
      i[1] = b;
    }
    operator const int*() const
    {
      return i;
    }
  };
}


namespace CTF {
  template<typename dtype>
  Matrix<dtype>::Matrix(int                       nrow_,
                        int                       ncol_,
                        World &                   world_,
                        CTF_int::algstrct const & sr_,
                        char const *              name_,
                        int                       profile_)
    : Tensor<dtype>(2, false, CTF_int::int2(nrow_, ncol_),  CTF_int::int2(NS, NS),
                           world_, sr_, name_, profile_) {
    nrow = nrow_;
    ncol = ncol_;
    symm = NS;
  }

  template<typename dtype>
  Matrix<dtype>::Matrix(int                       nrow_,
                        int                       ncol_,
                        int                       atr_,
                        World &                   world_,
                        CTF_int::algstrct const & sr_,
                        char const *              name_,
                        int                       profile_)
    : Tensor<dtype>(2, (atr_&4)>0, CTF_int::int2(nrow_, ncol_), CTF_int::int2(atr_&3, NS), 
                           world_, sr_, name_, profile_) {
    nrow = nrow_;
    ncol = ncol_;
    symm = atr_&3;
  }

  template<typename dtype>
  Matrix<dtype>::Matrix(int                       nrow_,
                        int                       ncol_,
                        World &                   world_,
                        char const *              name_,
                        int                       profile_,
                        CTF_int::algstrct const & sr_)
    : Tensor<dtype>(2, false, CTF_int::int2(nrow_, ncol_), CTF_int::int2(NS, NS),
                           world_, sr_, name_, profile_) {
    nrow = nrow_;
    ncol = ncol_;
    symm = 0;
  }


  template<typename dtype>
  Matrix<dtype>::Matrix(int                       nrow_,
                        int                       ncol_,
                        int                       atr_,
                        World &                   world_,
                        char const *              name_,
                        int                       profile_,
                        CTF_int::algstrct const & sr_)
    : Tensor<dtype>(2, (atr_&4)>0, CTF_int::int2(nrow_, ncol_), CTF_int::int2(atr_&3, NS), 
                           world_, sr_, name_, profile_) {
    nrow = nrow_;
    ncol = ncol_;
    symm = atr_&3;
  }

  template<typename dtype>
  Matrix<dtype>::Matrix(const Matrix<dtype> & A) 
    : Tensor<dtype>(A) {
    nrow = A.nrow;
    ncol = A.ncol;
    symm = A.symm;
/*    CTF_int::tensor::free_self();
    CTF_int::tensor::init(A.sr, A.order, A.lens, A.sym, A.wrld, 1, A.name, A.profile, A.is_sparse);
    return *this;*/
  }

}