submodule (parent) container
  implicit none

contains

    module function parent_weight(p) result(w)
      type(parent_type), intent(in) :: p
      real :: w

      w = p%mother**2 + p%father**2
    end function parent_weight

end submodule container
