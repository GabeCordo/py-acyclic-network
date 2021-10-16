from typing import Generic, TypeVar
from pyacyclicnet.core.types import errors

T = TypeVar('T')
G = TypeVar('G')

class Result:
    def __init__(self, value_g: Generic[T], exception_g: Generic[G]) -> None:
        """
            (Result, Generic, Exception) -> None
            :Constructor for the Any Class

            @returns nothing
            @exception returns InvalidResultClassArguments exception
        """
        # either value_g or exception_g should have a non None value (XOR)
        self.__value_g = value_g
        self.__exception_g = exception_g

    def is_valid(self) -> bool:
        """
            A Valid Result.class represents a state where a real value has
            been placed within the wrapper block

            @returns a boolean representing whether a non-exception value has been placed in the wrapper
        """
        if self.__value_g is None:
            return True
        return False

    def value(self):
        """
            Getter function for the non-exception value placed in the Result.class wrapper
        """
        return self.__value_g

    def exception(self) -> Exception:
        """
            Getter function for the exception value placed in the Result.class wrapper
        """
        return self.__exception_g

    def __eq__(self, other) -> bool:
        """
            (Result, Result) -> boolean
            :Compares two Result.class wrappers and evaluates the equality of either there
             generic data values OR the exceptions placed in the wrapper
        """
        # check that other.class is of type Result.class
        if not isinstance(other, Result):
            # other represents and Exception type we are trying to compare
            if isinstance(other, Exception):
                # check if the two exception types are the same
                return self.__exception_g == other
            elif isinstance(self.__value_g, other):
                # check if the two values we are given are the same
                return self.__value_g == other
            else:
                # if they are not both exception and the values are not the same type return false
                return False
        else:
            # do both contain non-exception data values
            if self.is_valid() and other.is_valid():
                # are there values of the same type and do they equal another
                return isinstance(self.__value_g, other.value()) and (self.__value_g == other.value())
            else:
                # check if the two exception values are the same type
                return self.__exception_g == other.exception()
