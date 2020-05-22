from moviepy.editor import *
import os
import glob
from PIL import Image
from resizeimage import resizeimage
from skimage.filters._gaussian import gaussian
import random as rd


# Функция для блюра картинок
def blur(image):
    return gaussian(image.astype(float), sigma=2)


# Указываем путь к фотографиям
img_dir = os.path.realpath("./movie")

# Получаем все фотографии формата .jpg
images = glob.glob('*.jpg')

# Изменяем размер фотографий, потому что
# нельзя создать клип из изображений
# разного размера
for m in images:
    with open(m, 'r+b') as f:
        with Image.open(f) as image:
            cover = resizeimage.resize_cover(image, [500, 700])
            cover.save(m, image.format)

# Делаем эффект блюра на некоторых изображениях
# для псевдо-рандомного выбора
# каждому изображению устанавливаем продолжительность 5 сек
# и сохраняем все в массив clips
clips = []
for m in images:
    if rd.randint(0, 1024) % 2 == 0:
        clips.append(ImageClip(m).fl_image(blur).set_duration(5))
    else:
        clips.append(ImageClip(m).set_duration(5))

# Соединяем все изображения в один клип
images_clip = concatenate_videoclips(clips, method="compose")

# Загружаем первое видео длительностью 30 секунд
trans_mem = VideoFileClip("trans.mp4").subclip("0:00:00", "0:00:30")

# Определяем размер видео, чтобы правильно
# расположить второе
w, h = moviesize = trans_mem.size

# Загружаем второе видео
# обрезаем его до длительности 30 секунд
# перемещаем его вниз справа
mozart = (VideoFileClip("violin.mp4", audio=True).
          subclip("0:00:35", "0:01:05").
          resize((w / 3, h / 3)).
          margin(6, color=(255, 0, 0)).
          margin(bottom=20, right=20, opacity=0).
          set_pos(('right', 'bottom')))

# Делаем TextClip, чтобы отобразить надпись сверху
txt_clip = (TextClip("Trans music who?", fontsize=70, color='white')
            .set_position('top')
            .set_duration(10))

# Соединяем первый и второй клип, а также
# добавляем нашу надпись (TextClip)
result = CompositeVideoClip([trans_mem, txt_clip, mozart])

# Загружаем аудио длинной 1 мин
vesna_audio = AudioFileClip("vesna.mp3").cutout("0:00:00", "0:01:00")

# Обрезаем видео на две части, чтобы добавить надпись
# только к последним десяти секундам
end_video1 = VideoFileClip("cats_video.mp4", audio=False)\
    .subclip("0:00:00", "0:01:00").set_audio(vesna_audio)
end_video2 = VideoFileClip("cats_video.mp4", audio=False)\
    .subclip("0:01:10", "0:01:20")

# Создаем надпись
the_end = (TextClip("Выполнила Ыклас Айгерим", fontsize=30, color='white')
           .set_position('bottom')
           .set_duration(10))

# Соединяем конец видео с надписью
end_video2 = CompositeVideoClip([the_end, end_video2])
final = concatenate([end_video1, the_end], method="compose")

# Соединяем все части нашего видео
result = concatenate([result, images_clip, final], method="compose")

# Обрезаем
result = result.subclip("0:00:00", "0:02:20")

# Записываем видео в .mp4 файл
result.write_videofile("vidclip_edited.mp4", fps=15)
