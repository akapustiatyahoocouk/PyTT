from typing import TypeAlias

import util_impl.Annotations
import util_impl.Metaclasses
import util_impl.Friends
import util_impl.UtilResources

staticproperty: TypeAlias = util_impl.Annotations.staticproperty
classproperty: TypeAlias = util_impl.Annotations.classproperty

ClassWithConstantsMeta: TypeAlias = util_impl.Metaclasses.ClassWithConstantsMeta
ClassWithConstants: TypeAlias = util_impl.Metaclasses.ClassWithConstants
ABCWithConstantsMeta: TypeAlias = util_impl.Metaclasses.ABCWithConstantsMeta
ABCWithConstants: TypeAlias = util_impl.Metaclasses.ABCWithConstants

FriendlyClassMeta: TypeAlias = util_impl.Friends.FriendlyClassMeta
FriendlyClass: TypeAlias = util_impl.Friends.FriendlyClass
FriendlyABCMeta: TypeAlias = util_impl.Friends.FriendlyABCMeta
FriendlyABC: TypeAlias = util_impl.Friends.FriendlyABC
UtilResources: TypeAlias = util_impl.UtilResources.UtilResources
