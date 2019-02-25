HEADER = """
%struct._IO_FILE = type { i32, i8*, i8*, i8*, i8*, i8*, i8*, i8*, i8*, i8*, i8*, i8*, %struct._IO_marker*, %struct._IO_FILE*, i32, i32, i64, i16, i8, [1 x i8], i8*, i64, i8*, i8*, i8*, i8*, i64, i32, [20 x i8] }
%struct._IO_marker = type { %struct._IO_marker*, %struct._IO_FILE*, i32 }

@.str   = private unnamed_addr constant [4 x i8] c"%d\\0A\\00"
@.str.1 = private unnamed_addr constant [4 x i8] c"%s\\0A\\00"
@.str.2 = private unnamed_addr constant [14 x i8] c"runtime error\\00"
@.str.readint = private unnamed_addr constant [3 x i8] c"%d\\00", align 1
@.str.3 = private unnamed_addr constant [1 x i8] zeroinitializer, align 1
@.str.4 = private unnamed_addr constant [22 x i8] c"readString error: %s\\0A\\00", align 1
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
  %1 = alloca i32, align 4
  %2 = alloca i8, align 1
  %3 = call i32 (i8*, ...) @__isoc99_scanf(i8* getelementptr inbounds ([3 x i8], [3 x i8]* @.str.readint, i32 0, i32 0), i32* %1)
  %4 = load %struct._IO_FILE*, %struct._IO_FILE** @stdin, align 8
  %5 = call i32 @_IO_getc(%struct._IO_FILE* %4)
  %6 = trunc i32 %5 to i8
  store i8 %6, i8* %2, align 1
  br label %7

; <label>:7:                                      ; preds = %17, %0
  %8 = load i8, i8* %2, align 1
  %9 = sext i8 %8 to i32
  %10 = icmp eq i32 %9, 32
  br i1 %10, label %15, label %11

; <label>:11:                                     ; preds = %7
  %12 = load i8, i8* %2, align 1
  %13 = sext i8 %12 to i32
  %14 = icmp eq i32 %13, 9
  br label %15

; <label>:15:                                     ; preds = %11, %7
  %16 = phi i1 [ true, %7 ], [ %14, %11 ]
  br i1 %16, label %17, label %21

; <label>:17:                                     ; preds = %15
  %18 = load %struct._IO_FILE*, %struct._IO_FILE** @stdin, align 8
  %19 = call i32 @_IO_getc(%struct._IO_FILE* %18)
  %20 = trunc i32 %19 to i8
  store i8 %20, i8* %2, align 1
  br label %7

; <label>:21:                                     ; preds = %15
  %22 = load i8, i8* %2, align 1
  %23 = sext i8 %22 to i32
  %24 = icmp eq i32 %23, 13
  br i1 %24, label %25, label %29

; <label>:25:                                     ; preds = %21
  %26 = load %struct._IO_FILE*, %struct._IO_FILE** @stdin, align 8
  %27 = call i32 @_IO_getc(%struct._IO_FILE* %26)
  %28 = trunc i32 %27 to i8
  store i8 %28, i8* %2, align 1
  br label %29

; <label>:29:                                     ; preds = %25, %21
  %30 = load i8, i8* %2, align 1
  %31 = sext i8 %30 to i32
  %32 = icmp ne i32 %31, -1
  br i1 %32, label %33, label %46

; <label>:33:                                     ; preds = %29
  %34 = load i8, i8* %2, align 1
  %35 = sext i8 %34 to i32
  %36 = icmp ne i32 %35, 10
  br i1 %36, label %37, label %46

; <label>:37:                                     ; preds = %33
  %38 = load i8, i8* %2, align 1
  %39 = sext i8 %38 to i32
  %40 = icmp ne i32 %39, 13
  br i1 %40, label %41, label %46

; <label>:41:                                     ; preds = %37
  %42 = load i8, i8* %2, align 1
  %43 = sext i8 %42 to i32
  %44 = load %struct._IO_FILE*, %struct._IO_FILE** @stdin, align 8
  %45 = call i32 @ungetc(i32 %43, %struct._IO_FILE* %44)
  br label %46

; <label>:46:                                     ; preds = %41, %37, %33, %29
  %47 = load i32, i32* %1, align 4
  ret i32 %47
}

declare  i32 @__isoc99_scanf(i8*, ...)

declare  i32 @_IO_getc(%struct._IO_FILE*) 

declare  i32 @ungetc(i32, %struct._IO_FILE*) 

define  i8* @readString() {
  %1 = alloca i8*, align 8
  %2 = alloca i8*, align 8
  %3 = alloca i64, align 8
  %4 = alloca i64, align 8
  store i8* null, i8** %2, align 8
  store i64 0, i64* %3, align 8
  %5 = load %struct._IO_FILE*, %struct._IO_FILE** @stdin, align 8
  %6 = call i64 @getline(i8** %2, i64* %3, %struct._IO_FILE* %5)
  store i64 %6, i64* %4, align 8
  %7 = load i64, i64* %4, align 8
  %8 = icmp sle i64 %7, 0
  br i1 %8, label %9, label %29

; <label>:9:                                      ; preds = %0
  %10 = load i8*, i8** %2, align 8
  %11 = icmp ne i8* %10, null
  br i1 %11, label %12, label %14

; <label>:12:                                     ; preds = %9
  %13 = load i8*, i8** %2, align 8
  call void @free(i8* %13) #5
  br label %14

; <label>:14:                                     ; preds = %12, %9
  %15 = load i64, i64* %4, align 8
  %16 = icmp eq i64 %15, 0
  br i1 %16, label %20, label %17

; <label>:17:                                     ; preds = %14
  %18 = load i64, i64* %4, align 8
  %19 = icmp eq i64 %18, -1
  br i1 %19, label %20, label %21

; <label>:20:                                     ; preds = %17, %14
  store i8* getelementptr inbounds ([1 x i8], [1 x i8]* @.str.3, i32 0, i32 0), i8** %1, align 8
  br label %60

; <label>:21:                                     ; preds = %17
  %22 = load i64, i64* %4, align 8
  %23 = trunc i64 %22 to i32
  %24 = call i8* @strerror(i32 %23) #5
  %25 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([22 x i8], [22 x i8]* @.str.4, i32 0, i32 0), i8* %24)
  %26 = load i64, i64* %4, align 8
  %27 = sub nsw i64 0, %26
  %28 = trunc i64 %27 to i32
  call void @exit(i32 %28) #4
  unreachable

; <label>:29:                                     ; preds = %0
  %30 = load i8*, i8** %2, align 8
  %31 = load i64, i64* %4, align 8
  %32 = sub nsw i64 %31, 1
  %33 = getelementptr inbounds i8, i8* %30, i64 %32
  %34 = load i8, i8* %33, align 1
  %35 = sext i8 %34 to i32
  %36 = icmp eq i32 %35, 10
  br i1 %36, label %37, label %42

; <label>:37:                                     ; preds = %29
  %38 = load i8*, i8** %2, align 8
  %39 = load i64, i64* %4, align 8
  %40 = add nsw i64 %39, -1
  store i64 %40, i64* %4, align 8
  %41 = getelementptr inbounds i8, i8* %38, i64 %40
  store i8 0, i8* %41, align 1
  br label %42

; <label>:42:                                     ; preds = %37, %29
  %43 = load i64, i64* %4, align 8
  %44 = icmp ne i64 %43, 0
  br i1 %44, label %45, label %58

; <label>:45:                                     ; preds = %42
  %46 = load i8*, i8** %2, align 8
  %47 = load i64, i64* %4, align 8
  %48 = sub nsw i64 %47, 1
  %49 = getelementptr inbounds i8, i8* %46, i64 %48
  %50 = load i8, i8* %49, align 1
  %51 = sext i8 %50 to i32
  %52 = icmp eq i32 %51, 13
  br i1 %52, label %53, label %58

; <label>:53:                                     ; preds = %45
  %54 = load i8*, i8** %2, align 8
  %55 = load i64, i64* %4, align 8
  %56 = add nsw i64 %55, -1
  store i64 %56, i64* %4, align 8
  %57 = getelementptr inbounds i8, i8* %54, i64 %56
  store i8 0, i8* %57, align 1
  br label %58

; <label>:58:                                     ; preds = %53, %45, %42
  %59 = load i8*, i8** %2, align 8
  store i8* %59, i8** %1, align 8
  br label %60

; <label>:60:                                     ; preds = %58, %20
  %61 = load i8*, i8** %1, align 8
  ret i8* %61
}

declare  i8* @strerror(i32)

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

"""
