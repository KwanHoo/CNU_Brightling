import glob
import os
import shutil
from tkinter import *  # __all__ 에 저장된 모듈 임포트됨
import tkinter.ttk as ttk
from tkinter import filedialog  # 파일 불로오는 기능 (서브 모듈이라 *로 안불러와짐)
import tkinter.messagebox as msgbox  # 메세지 박스 사용시 불러옴
from PIL import Image  # 이미지 관련 모듈
from threading import Thread
from multiprocessing import Process
from enlighten_inference import EnlightenOnnxModel
import cv2
import time
import numpy as np
import detect_custom
import torch
##
# from detect_custom import im0
# import sys

model = EnlightenOnnxModel()
root = Tk()
root.title("야간 영상 화질 개선 및 객체탐지")  # 제목
root.option_add("*Font", "맑은고딕 13")

image_list = []
count = 0


# 파일 추가 (선택한 파일 모두)
def add_file():  # 복수개의 파일 선택
    global count
    global image_list
    files = filedialog.askopenfilenames(title="개선시킬 저조도 이미지 파일을 선택하세요", \
                                        filetypes=(("미디어 파일", "*.png;*.jpg;*.mp4"), ("모든 파일", "*.*")), \
                                        initialdir="C:/Users/LAND/Desktop")

    # 사용자가 선택한 파일 목록
    for file in files:
        list_file.insert(END, file)  # 리스트 파일 프레임에 추가
        image_list.append(file)
        count += 1
    print(count)


# 선택 파일 목록에서 삭제
def del_file():
    global image_list
    global count

    for index in reversed(list_file.curselection()):  # reversed : 거꾸로 반환해줌 (인덱스의 경우 뒤에서부터 재껴야됨)
        if count > 0:
            count -= 1
        list_file.delete(index)
        del image_list[index]
    print(count)

    return image_list

def del_all_file():
    global count
    global image_list
    for i in range(count+1):
        list_file.delete(0)

    count = 0
    image_list = []
    # for index in list_file:  # reversed : 거꾸로 반환해줌 (인덱스의 경우 뒤에서부터 재껴야됨)
    #     list_file.delete(index)


# 선택 영상 파일 미리보기 오픈
def show_file():
    for index in reversed(list_file.curselection()):
        prev = image_list[int(index)]
        # replace_prev = prev.replace('\\','/')
        # str_prev = 'r\'{}\''.format(replace_prev)

        if prev.split(".")[-1] == ("mp4" or "avi" or "gif"):
            prev_video = cv2.VideoCapture(prev, apiPreference=None)
            fps = prev_video.get(cv2.CAP_PROP_FPS)
            while prev_video.read() and prev_video.get(cv2.CAP_PROP_POS_FRAMES) != prev_video.get(cv2.CAP_PROP_FRAME_COUNT):
                run, frame = prev_video.read()
                if not run:
                    msgbox.showwarning("경고", "재생이 불가능합니다.")
                    break
                cv2.imshow('preview(press Q, stop, then press any key -> close)', frame)
                if cv2.waitKey(int(1000/fps)) & 0xFF == ord('q'):
                    prev_video.release()
                    cv2.destroyAllWindows()
                    break

        else:
            prev_image = cv2.imread(prev, cv2.IMREAD_COLOR)
            (h, w, c) = prev_image.shape
            h = h/w
            size = 500
            prev_image = cv2.resize(prev_image, (size, int(size*h)))
            cv2.imshow('preview(press any key for close).', prev_image)
            cv2.waitKey()
            cv2.destroyAllWindows()


# 저장 경로 (폴더)
def brows_dest_path():
    folder_selected = filedialog.askdirectory()  # 폴더 선택
    if folder_selected == '':  # 사용자가 취소를 누를 때
        print('폴더 선택 취소')
        return
    txt_dest_path.delete(0, END)  # 먼저 저장되어있는거 삭제
    txt_dest_path.insert(0, folder_selected)  # 경로란에 들어가짐


###########
# 이미지 조도 개선
def LLE():
    try:  # 예외처리, 버그(저장 문제)

        # 포맷
        # img_format = cmb_format.get().lower()  # 확장자 값 받아와서 소문자로 변경
        curr_time = "LLE_"+time.strftime("%Y%m%d_%H%M%S")  # 시간값

        os.mkdir(os.path.join(txt_dest_path.get(), curr_time))
        for i in range(count):
            file_name = list_file.get(str(i))
            origin_name = file_name.split("/")[-1]
            # print(file_name)
            print(file_name)
            images = cv2.imread(str(file_name))
            processed = model.predict(images)

            file_name = origin_name
            dest_path = os.path.join(txt_dest_path.get(), curr_time, file_name)  # 저장경로 설정
            # print(dest_path)

            cv2.imwrite(dest_path, processed)

        askopendir = msgbox.askokcancel("알림", "조도개선이 완료되었습니다. 폴더를 열어보시겠습니까?")
        if askopendir:
            # 이미지 미리보기
            os.startfile(txt_dest_path.get()+"/"+curr_time)
            # cv2.imshow('result', processed)
            # cv2.waitKey()
            # cv2.destroyAllWindows()

    except Exception as err:  # 예외처리
        msgbox.showerror("에러", err)


def obj_detect():
    device_selector = cmb_format.get().lower()
    if device_selector == 'gpu':
        device_selector = 0

    curr_time = time.strftime("%Y%m%d %H%M%S")  # 시간값
    name = 'OD_'+curr_time

    try:
        for media in range(len(image_list)):
            detect_custom.run(weights='./best_200.pt',
                              source=image_list[media],
                              imgsz=640,
                              conf_thres=0.2,
                              iou_thres=0.45,
                              max_det=1000,
                              device=device_selector,
                              view_img=False,
                              save_txt=False,
                              save_conf=False,
                              save_crop=False,
                              nosave=False,
                              classes=None,
                              agnostic_nms=False,
                              augment=False,
                              visualize=False,
                              update=False,
                              project=txt_dest_path.get(),
                              name=name,
                              exist_ok=True,
                              line_thickness=2,
                              hide_labels=False,
                              hide_conf=False,
                              half=False)
        askopendir = msgbox.askokcancel("알림", "객체탐지가 완료되었습니다. 폴더를 열어보시겠습니까?")
        if askopendir:
            os.startfile(txt_dest_path.get()+"/"+name)
    except Exception as err:  # 예외처리
        msgbox.showerror("에러", err)


def logging():
    device_selector = cmb_format.get().lower()
    if device_selector == 'gpu':
        device_selector = 0

    curr_time = time.strftime("%Y%m%d %H%M%S")  # 시간값
    name = 'LOG_'+curr_time
    try:
        for media in range(len(image_list)):
            detect_custom.run(weights='./best_200.pt',
                              source=image_list[media],
                              imgsz=640,
                              conf_thres=0.2,
                              iou_thres=0.45,
                              max_det=1000,
                              device=device_selector,
                              view_img=False,
                              save_txt=True,
                              save_conf=False,
                              save_crop=False,
                              nosave=False,
                              classes=None,
                              agnostic_nms=False,
                              augment=False,
                              visualize=False,
                              update=False,
                              project=txt_dest_path.get(),
                              name=name,
                              exist_ok=True,
                              line_thickness=2,
                              hide_labels=False,
                              hide_conf=False,
                              half=False)
            file_position = image_list[media]
            log_path = os.path.join(txt_dest_path.get(), name) + '\log\*.txt'
            if file_position.split(".")[-1] == "mp4" or "avi":
                video = cv2.VideoCapture(image_list[media])
                file_name = file_position.split("/")[-1].split(".")[0]  # 파일명(확장자 제외) 추출
                fps = video.get(cv2.CAP_PROP_FPS)
                total_frame = video.get(cv2.CAP_PROP_FRAME_COUNT)
                video_length = total_frame/fps
                object_frame_count = glob.glob(log_path)
                detected_frame = []
                for literal in range(len(object_frame_count)):
                    detected_frame.append(int(object_frame_count[literal].split("\\")[-1][len(file_name)+1:-4]))
                    # print(detected_frame.append(int(object_frame_count[literal].split("\\")[1][len(file_name) + 1:-4])), "done")
                    # 파일명 저장 규칙이 확장자 없는 파일명이므로 .txt인 -4까지는 출력 안함.
                detected_frame = sorted(detected_frame)  # 오름차순 정렬
                second = []
                print("총", video_length, "초의 비디오에서 약", round(len(object_frame_count) / fps, 1),
                      "초 동안 탐지되었으며 구간은 다음과 같습니다")
                for i in range(len(detected_frame) - 1):
                    if int(detected_frame[i] / fps) == int(detected_frame[i + 1] / fps):
                        continue
                    second.append((int(detected_frame[i] / fps)))
                print(second, "초")
                f = open(txt_dest_path.get()+"/"+name+"/"+file_name+"_log.txt", "w")
                f.write("탐지된 구간(초): %s" % second)
                f.close()
                shutil.rmtree(txt_dest_path.get()+"/"+name+"/log")

        askopendir = msgbox.askokcancel("알림", "로그 기록이 완료되었습니다. 폴더를 열어보시겠습니까?")
        if askopendir:
            # 이미지 미리보기
            os.startfile(txt_dest_path.get()+"/"+name)
    except Exception as err:  # 예외처리
        msgbox.showerror("에러", err)


def RTdetectStart():
    device_selector = 'cpu'
    if torch.cuda.is_available():
        device_selector = 0
    curr_time = time.strftime("%Y%m%d %H%M%S")  # 시간값
    name = 'RTDetect_' + curr_time

    video = cv2.VideoCapture(0).read()
    video1 = cv2.VideoCapture(1).read()
    video2 = cv2.VideoCapture(2).read()

    if not video[0] and not video1[0] and not video2[0]:
        msgbox.showwarning("알림", "연결된 웹캠이 없습니다.")
    else:
        if video[0]:
            source = '0'
        elif video1[0]:
            source = '1'
        elif video2[0]:
            source = '2'
        try:
            detect_custom.run(weights='./best_200.pt',
                              source=source,
                              imgsz=640,
                              conf_thres=0.25,
                              iou_thres=0.45,
                              max_det=1000,
                              device=device_selector,
                              view_img=False,
                              save_txt=True,
                              save_conf=False,
                              save_crop=False,
                              nosave=False,
                              classes=None,
                              agnostic_nms=False,
                              augment=False,
                              visualize=False,
                              update=False,
                              project=txt_dest_path.get(),
                              name=name,
                              exist_ok=False,
                              line_thickness=1,
                              hide_labels=False,
                              hide_conf=False,
                              half=False)
        except Exception as err:
            msgbox.showerror("알림", "실시간 탐지에 실패했습니다.\n에러내용: %s" % err)




def RTdetectEnd():
    pass

def emptyrt():
    pass


# 저조도 개선
def start_LLE():
    # 각 옵션 값들 확인
    # print("포맷 : ", cmb_format.get())

    # 파일 목록 확인
    if list_file.size() == 0:  # 파일 선택 없을시 경고메세지
        msgbox.showwarning("경고", "파일을 선택하세요")
        return

    # 저장 경로 확인
    if len(txt_dest_path.get()) == 0:
        msgbox.showwarning("경고", "저장 경로를 선택하세요")
        return

    ##########
    # 저조도 개선 작업
    LLE()


def start_obj_detect():
    # 각 옵션 값들 확인
    # print("포맷 : ", cmb_format.get())

    # 파일 목록 확인
    if list_file.size() == 0:  # 파일 선택 없을시 경고메세지
        msgbox.showwarning("경고", "파일을 선택하세요")
        return

    # 저장 경로 확인
    if len(txt_dest_path.get()) == 0:
        msgbox.showwarning("경고", "저장 경로를 선택하세요")
        return

    obj_detect()


def start_logging():
    # 각 옵션 값들 확인
    # print("포맷 : ", cmb_format.get())

    # 파일 목록 확인
    if list_file.size() == 0:  # 파일 선택 없을시 경고메세지
        msgbox.showwarning("경고", "파일을 선택하세요")
        return

    # 저장 경로 확인
    if len(txt_dest_path.get()) == 0:
        msgbox.showwarning("경고", "저장 경로를 선택하세요")
        return

    logging()



# th1 = Process(target=RTdetectStart)

# 실시간 탐지 프레임
realtime_frame = LabelFrame(root, text="CCTV 화면")
realtime_frame.pack(fill="x", padx=5, pady=1, side="left")

btn_rtstart_file = Label(realtime_frame, padx=5, pady=5, width=50, height=20, text="실시간 탐지를 사용하고 있지 않습니다",)
btn_rtstart_file.pack(side="top", padx=5, pady=10, ipady=4)

btn_rtstart_file = Button(realtime_frame, padx=5, pady=5, width=12, text="실시간탐지시작", command=RTdetectStart)
btn_rtstart_file.pack(side="left", padx=5, pady=15, ipady=4, ipadx=18)

btn_rtend_file = Button(realtime_frame, padx=5, pady=5, width=12, text="실시간탐지종료", command=RTdetectEnd)
btn_rtend_file.pack(side="right", padx=5, pady=15, ipady=4, ipadx=18)

# 파일 프레임 (파일 추가, 선택 삭제, 선택 확인)

file_frame = Frame(root)
file_frame.pack(fill="x", padx=5, pady=5)

btn_add_file = Button(file_frame, padx=5, pady=5, width=12, text="파일추가", command=add_file)
btn_add_file.pack(side="left", padx=5)

btn_del_file = Button(file_frame, padx=5, pady=5, width=12, text="파일삭제", command=del_file)
btn_del_file.pack(side="left", padx=5)

btn_delall_file = Button(file_frame, padx=5, pady=5, width=12, text="전체삭제", command=del_all_file)
btn_delall_file.pack(side="left", padx=5)

btn_show_file = Button(file_frame, padx=5, pady=5, width=12, text="영상확인", command=show_file)
btn_show_file.pack(side="right", padx=5)

# 리스트 프레임
list_frame = LabelFrame(root, text="upload 파일 리스트 목록")
list_frame.pack(fill="both", padx=5, pady=5)

scrollbar = Scrollbar(list_frame)
scrollbar.pack(side="right", fill="y")

list_file = Listbox(list_frame, selectmode="extended", height=15,
                    yscrollcommand=scrollbar.set)  # yscrollcommand=scrollbar.set 이걸 해줘야 서로 맵핑이됨
list_file.pack(side="left", fill="both", expand=True)
scrollbar.config(command=list_file.yview)

# 저장 경로 프레임
path_frame = LabelFrame(root, text="저장경로")
path_frame.pack(fill="x", padx=5, pady=5, ipady=5)  # fill="x"  : 프레임 늘려줌

txt_dest_path = Entry(path_frame)
txt_dest_path.pack(side="left", fill="x", expand=True, padx=5, pady=5, ipady=4, ipadx=20)  # ipad : 안쪽 패딩

# 파일포맷 옵션 콤보
if torch.cuda.is_available():
    opt_format = ["CPU", "GPU"]
    cmb_format = ttk.Combobox(path_frame, state="readonly", values=opt_format, width=5)
    cmb_format.current(0)  # 첫번째 값 기본선택
else:
    # cmb_format = ttk.Label(path_frame, text="CPU")
    opt_format = ["CPU"]
    cmb_format = ttk.Combobox(path_frame, state="readonly", values=opt_format, width=5)
    cmb_format.current(0)


cmb_format.pack(side="right", padx=5, pady=5)

# 파일 포맷 옵션
# 파일포맷 옵션 레이블
lbl_format = Label(path_frame, text="사용 도구:", width=8)
lbl_format.pack(side="right", padx=5, pady=5)

btn_dest_path = Button(path_frame, text="찾아보기", width=10, command=brows_dest_path)
btn_dest_path.pack(side="right", padx=5, pady=5)

# 실행 프레임
frame_run = LabelFrame(root, text="기능")
frame_run.pack(fill="x", padx=5, pady=5)

btn_close = Button(frame_run, padx=5, pady=5, text="프로그램종료", width=12, command=root.quit)
btn_close.pack(side="right", padx=5, pady=5)

btn_LLE = Button(frame_run, padx=5, pady=5, text="저조도개선", width=12, command=start_LLE)
btn_LLE.pack(side="left", padx=5, pady=5)

btn_OD = Button(frame_run, padx=5, pady=5, text="객체탐지", width=12, command=start_obj_detect)
btn_OD.pack(side="left", padx=5, pady=5)

btn_log = Button(frame_run, padx=5, pady=5, text="로그기록", width=12, command=start_logging)
btn_log.pack(side="left", padx=5, pady=5)


# 진행도 추가됐음 해서 추가해봄.. 지워도 OK
# frame_progress = LabelFrame(root, text="진행도")
# frame_progress.pack(fill="x", padx=5, pady=5)
# progressbar = ttk.Progressbar(frame_progress, maximum=100, value=0, variable=1, mode="determinate")
# progressbar.pack(fill="x", padx=5, pady=5)


root.resizable(False, False)  # x(너비), y(높이) 값 변경 불가 (창 크기 변경 불가)
root.mainloop()  # 창이 닫히지 않도록 해줌