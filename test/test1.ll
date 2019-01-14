
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

declare i8* @strdup(i8*)

declare i64 @getline(i8**, i64*, %struct._IO_FILE*)

declare noalias i8* @malloc(i64)

declare void @free(i8* nocapture)

define i32 @main() {
call void @printInt(i32 123123)
ret i32 0
}
define i32 @sernik(i32, i8*, i32) {
call void @printInt(i32 123123)
ret i32 0
}
