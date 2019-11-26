from PIL import Image


def main():
    # if len(sys.argv) != 4:
    #     print("Error: Wrong argv.")
    #     exit()

    ppm_name = 'myppm.ppm'
    img_name = 'Tux.jpg'

    result_ppm = 'result.ppm'
    result_img = 'result.jpg'

    im = Image.open(img_name)
    im.save(ppm_name, 'ppm')

    im = Image.open(ppm_name)
    im.save(result_img, 'jpeg')

    file = open(ppm_name, 'rb')
    content = file.read()
    im = Image.open(result_img)
    im.save(result_ppm, 'ppm')
    file2 = open(result_ppm, 'rb')
    content2 = file2.read()
    exit()


if __name__ == "__main__":
    main()
