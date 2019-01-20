
%struct._IO_FILE = type { i32, i8*, i8*, i8*, i8*, i8*, i8*, i8*, i8*, i8*, i8*, i8*, %struct._IO_marker*, %struct._IO_FILE*, i32, i32, i64, i16, i8, [1 x i8], i8*, i64, i8*, i8*, i8*, i8*, i64, i32, [20 x i8] }
%struct._IO_marker = type { %struct._IO_marker*, %struct._IO_FILE*, i32 }

@.str   = private unnamed_addr constant [4 x i8] c"%d\0A\00"
@.str.1 = private unnamed_addr constant [4 x i8] c"%s\0A\00"
@.str.2 = private unnamed_addr constant [14 x i8] c"runtime error\00"
@stdin = external global %struct._IO_FILE*, align 8


define void @printInt(i32) {
  %2 = alloca i32
  store i32 %0, i32* %2
  %3 = load i32, i32* %2
  %4 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([4 x i8], [4 x i8]* @.str, i32 0, i32 0), i32 %3)
  ret void
}

declare i32 @printf(i8*, ...) 

define void @printString(i8*) {
  %2 = alloca i8*, align 8
  store i8* %0, i8** %2, align 8
  %3 = load i8*, i8** %2, align 8
  %4 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([4 x i8], [4 x i8]* @.str.1, i32 0, i32 0), i8* %3)
  ret void
}

define void @error()  {
  %1 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([14 x i8], [14 x i8]* @.str.2, i32 0, i32 0))
  call void @exit(i32 0)
  unreachable
  ret void
}

declare void @exit(i32)

define i32 @readInt() {
  %1 = alloca i32
  %2 = call i32 (i8*, ...) @scanf(i8* getelementptr inbounds ([4 x i8], [4 x i8]* @.str, i32 0, i32 0), i32* %1)
  %3 = load i32, i32* %1
  ret i32 %3
}

declare i32 @scanf(i8*, ...)

define  i8* @readString() {
  %1 = alloca i8*, align 8
  %2 = alloca i32, align 4
  %3 = alloca i64, align 8
  store i8* null, i8** %1, align 8
  %4 = load %struct._IO_FILE*, %struct._IO_FILE** @stdin, align 8
  %5 = call i64 @getline(i8** %1, i64* %3, %struct._IO_FILE* %4)
  %6 = trunc i64 %5 to i32
  store i32 %6, i32* %2, align 4
  %7 = load i8*, i8** %1, align 8
  %8 = call noalias i8* @strdup(i8* %7) #5
  ret i8* %8 
}

define i8* @concat(i8*, i8*) {
  %3 = tail call i64 @strlen(i8* %0)
  %4 = tail call i64 @strlen(i8* %1)
  %5 = add i64 %3, 1
  %6 = add i64 %5, %4
  %7 = tail call noalias i8* @malloc(i64 %6)
  %8 = tail call i8* @strcpy(i8* %7, i8* %0)
  %9 = tail call i8* @strcat(i8* %7, i8* %1)
  ret i8* %7
}

declare i64 @strlen(i8*)

declare i8* @strcpy(i8*, i8*)

declare i8* @strcat(i8*, i8*)

declare i8* @strdup(i8*)

declare i64 @getline(i8**, i64*, %struct._IO_FILE*)

declare noalias i8* @malloc(i64)

declare void @free(i8* nocapture)

@s0 = internal constant [1 x i8] c"\00"
@s1 = internal constant [2 x i8] c"=\00"
@s2 = internal constant [9 x i8] c"hello */\00"
@s3 = internal constant [9 x i8] c"/* world\00"

define i32 @main() {
%1 = add i32 10, 0
%2 = call i32 @fac(i32 %1)
call void @printInt(i32 %2)
%3 = add i32 10, 0
%4 = call i32 @rfac(i32 %3)
call void @printInt(i32 %4)
%5 = add i32 10, 0
%6 = call i32 @mfac(i32 %5)
call void @printInt(i32 %6)
%7 = add i32 10, 0
%8 = call i32 @ifac(i32 %7)
call void @printInt(i32 %8)
%9 = alloca i8*
%10 = bitcast [1 x i8]* @s0 to i8*
%11 = alloca i32
%12 = add i32 10, 0
store i32 %12, i32* %11
%13 = alloca i32
%14 = add i32 1, 0
store i32 %14, i32* %13
br label %L1
L1:
%15 = load i32, i32* %11
%16 = add i32 0, 0
%17 = icmp sgt i32 %15, %16
br i1 %17, label %L2, label %L3
L2:
%18 = load i32, i32* %13
%19 = load i32, i32* %11
%20 = mul nsw i32 %18, %19
store i32 %20, i32* %13
%21 = load i32, i32* %11
%22 = sub nsw i32 %21, 1
store i32  %22, i32* %11
br label %L1
L3:
%23 = load i32, i32* %13
call void @printInt(i32 %23)
%24 = bitcast [2 x i8]* @s1 to i8*
%25 = add i32 60, 0
%26 = call i8* @repStr(i8* %24, i32 %25)
call void @printString(i8* %26)
%27 = bitcast [9 x i8]* @s2 to i8*
call void @printString(i8* %27)
%28 = bitcast [9 x i8]* @s3 to i8*
call void @printString(i8* %28)
%29 = add i32 0, 0
ret i32 %29
ret i32 0
}
define i32 @fac(i32) {
%2 = alloca i32
store i32 %0, i32* %2
%3 = alloca i32
store i32 0, i32* %3
%4 = alloca i32
store i32 0, i32* %4
%5 = add i32 1, 0
store i32 %5, i32* %3
%6 = load i32, i32* %2
store i32 %6, i32* %4
br label %L4
L4:
%7 = load i32, i32* %4
%8 = add i32 0, 0
%9 = icmp sgt i32 %7, %8
br i1 %9, label %L5, label %L6
L5:
%10 = load i32, i32* %3
%11 = load i32, i32* %4
%12 = mul nsw i32 %10, %11
store i32 %12, i32* %3
%13 = load i32, i32* %4
%14 = add i32 1, 0
%15 = sub nsw i32 %13, %14
store i32 %15, i32* %4
br label %L4
L6:
%16 = load i32, i32* %3
ret i32 %16
ret i32 0
}
define i32 @rfac(i32) {
%2 = alloca i32
store i32 %0, i32* %2
%3 = load i32, i32* %2
%4 = add i32 0, 0
%5 = icmp eq i32 %3, %4
br i1 %5, label %L7, label %L8
L7:
%6 = add i32 1, 0
ret i32 %6
br label %L9
L8:
%8 = load i32, i32* %2
%9 = load i32, i32* %2
%10 = add i32 1, 0
%11 = sub nsw i32 %9, %10
%12 = call i32 @rfac(i32 %11)
%13 = mul nsw i32 %8, %12
ret i32 %13
br label %L9
L9:
ret i32 0
}
define i32 @mfac(i32) {
%2 = alloca i32
store i32 %0, i32* %2
%3 = load i32, i32* %2
%4 = add i32 0, 0
%5 = icmp eq i32 %3, %4
br i1 %5, label %L10, label %L11
L10:
%6 = add i32 1, 0
ret i32 %6
br label %L12
L11:
%8 = load i32, i32* %2
%9 = load i32, i32* %2
%10 = add i32 1, 0
%11 = sub nsw i32 %9, %10
%12 = call i32 @nfac(i32 %11)
%13 = mul nsw i32 %8, %12
ret i32 %13
br label %L12
L12:
ret i32 0
}
define i32 @nfac(i32) {
%2 = alloca i32
store i32 %0, i32* %2
%3 = load i32, i32* %2
%4 = add i32 0, 0
%5 = icmp ne i32 %3, %4
br i1 %5, label %L13, label %L14
L13:
%6 = load i32, i32* %2
%7 = add i32 1, 0
%8 = sub nsw i32 %6, %7
%9 = call i32 @mfac(i32 %8)
%10 = load i32, i32* %2
%11 = mul nsw i32 %9, %10
ret i32 %11
br label %L15
L14:
%13 = add i32 1, 0
ret i32 %13
br label %L15
L15:
ret i32 0
}
define i32 @ifac(i32) {
%2 = alloca i32
store i32 %0, i32* %2
%3 = add i32 1, 0
%4 = load i32, i32* %2
%5 = call i32 @ifac2f(i32 %3, i32 %4)
ret i32 %5
ret i32 0
}
define i32 @ifac2f(i32, i32) {
%3 = alloca i32
store i32 %0, i32* %3
%4 = alloca i32
store i32 %1, i32* %4
%5 = load i32, i32* %3
%6 = load i32, i32* %4
%7 = icmp eq i32 %5, %6
br i1 %7, label %L16, label %L17
L16:
%8 = load i32, i32* %3
ret i32 %8
br label %L18
L17:
br label %L18
L18:
%10 = load i32, i32* %3
%11 = load i32, i32* %4
%12 = icmp sgt i32 %10, %11
br i1 %12, label %L19, label %L20
L19:
%13 = add i32 1, 0
ret i32 %13
br label %L21
L20:
br label %L21
L21:
%15 = alloca i32
store i32 0, i32* %15
%16 = load i32, i32* %3
%17 = load i32, i32* %4
%18 = add nsw i32 %16, %17
%19 = add i32 2, 0
%20 = sdiv i32 %18, %19
store i32 %20, i32* %15
%21 = load i32, i32* %3
%22 = load i32, i32* %15
%23 = call i32 @ifac2f(i32 %21, i32 %22)
%24 = load i32, i32* %15
%25 = add i32 1, 0
%26 = add nsw i32 %24, %25
%27 = load i32, i32* %4
%28 = call i32 @ifac2f(i32 %26, i32 %27)
%29 = mul nsw i32 %23, %28
ret i32 %29
ret i32 0
}
define i8* @repStr(i8*, i32) {
%3 = alloca i8*
store i8* %0, i8** %3
%4 = alloca i32
store i32 %1, i32* %4
%5 = alloca i8*
%6 = bitcast [1 x i8]* @s0 to i8*
store i8* %6, i8** %5
%7 = alloca i32
%8 = add i32 0, 0
store i32 %8, i32* %7
br label %L22
L22:
%9 = load i32, i32* %7
%10 = load i32, i32* %4
%11 = icmp slt i32 %9, %10
br i1 %11, label %L23, label %L24
L23:
%12 = load i8*, i8** %5
%13 = load i8*, i8** %3
%14 = call i8* @concat(i8* %12, i8* %13)
store i8* %14, i8** %5
%15 = load i32, i32* %7
%16 = add nsw i32 %15, 1
store i32  %16, i32* %7
br label %L22
L24:
%17 = load i8*, i8** %5
ret i8* %17
%19 = bitcast [1 x i8]* @s0 to i8*
ret i8* %19
}
