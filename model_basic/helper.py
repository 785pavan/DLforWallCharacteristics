def one_hot_encode(mask, palette):
    """
    Converts mask to a one-hot encoding specified by the semantic map.
    """
    one_hot_map = []
    for colour in palette:
        class_map = tf.reduce_all(tf.equal(mask, colour), axis=-1)
        one_hot_map.append(class_map)
    one_hot_map = tf.stack(one_hot_map, axis=-1)
    one_hot_map = tf.cast(one_hot_map, tf.float32)

    return one_hot_map


def patch_maker(savedir, path, filename, target_size=(256, 256)):
    '''opens one images at a time and saves them into patches of given hight and width.
    It also handels RGBA format issues
    @perams: savedir: directory to save patches
             path: path to get the big images from'''
    if not os.path.isdir(savedir):
        os.mkdir(savedir)
    img = Image.open(path + filename)
    width, height = img.size

    start_pos = start_x, start_y = (0, 0)
    cropped_image_size = w, h = target_size

    new_name = filename.split('.')[0]
    frame_num = 1
    for col_i in tqdm_notebook(range(0, width, w)):
        for row_i in range(0, height, h):
            crop = img.crop((col_i, row_i, col_i + w, row_i + h))
            save_to = os.path.join(savedir, new_name + "_{:04}.jpg")
            if crop.mode in ('RGBA', 'LA'):
                background = Image.new(crop.mode[:-1], crop.size, (255, 255, 255))
                background.paste(crop, crop.split()[-1])
                crop = background
            crop.save(save_to.format(frame_num))
            frame_num += 1


def save_patches(savedir, path, images, masks):
    '''Save patches using some axilary function above'''
    if not os.path.isdir(savedir):
        os.makedirs(savedir)
    path_im = path + images
    path_ms = path + masks
    ids = next(os.walk(path_ms))[2]
    for n, id_ in tqdm_notebook(enumerate(ids), total=len(ids)):
        '''image pathing'''
        print(id_.replace('.png', ''))
        patch_maker(savedir + 'images/images', path_im, id_.replace('.png', '.tif'))

        '''mask patching'''
        patch_maker(savedir + 'masks/masks', path_ms, id_)


def preprossesing_image(image, is_image_name=True):
    ''' takes either image filename or file itself and returns a ndarray and width and height

    @params: image = filename or image
             is_image_name = True is its a filename or
                             False if passing image directly'''
    if is_image_name:
        image = Image.open(image)
    if not type(image).__module__ == np.__name__:
        if image.mode in ('RGBA', 'LA'):
            background = Image.new(image.mode[:-1], image.size, (255, 255, 255))
            background.paste(image, image.split()[-1])
            image = background
        image = np.array(image, dtype=np.float64) / 255.
    w, h, d = original_shape = image.shape
    assert d == 3
    image_array = np.reshape(image, (w * h, d))
    return image_array, w, h


def display_image_with_labels(labels, w, h, centers):
    ''' convert image back into rgb format from labels
    @params: labels = w x h x 1 ndarray
             centers = cookbook for reference '''
    image = np.zeros((w, h, 3))
    for i, row in enumerate(labels):
        for j, col in enumerate(row):
            image[i][j] = centers[int(col)]
    return image


def get_labels(image, is_image_name=True):
    ''' converts image into labels using pretrained kmeans algorithm'''
    image_array, w, h = preprossesing_image(image, is_image_name=is_image_name)
    label = reshape_label(kmeans_color_palette_2.predict(image_array), w, h)
    return label, w, h


def get_image(label, w=None, h=None, cookbook=kmeans_color_palette_2.cluster_centers_):
    ''' coverts labels back to image'''
    '''if w==None or h==None:
        w, h, _ = label.shape'''
    image = display_image_with_labels(label, w, h, cookbook)
    return image


def create_mask_set(train_gen=train_gen):
    for images, masks in train_gen:
        new_lables = []
        for mask in masks:
            label, w, h = get_labels(mask, is_image_name=False)
            new_lables.append(label)
        yield (images, np.asarray(new_lables))


def reshape_label(labels, w, h):
    ''' takes 1d array of labels and reshapes it into orignal image height and width
    @params: labels = label
             w = width of image
             h = height of image'''

    lbl_reshaped = np.zeros((w, h, 1))
    labels_idx = 0
    for i in range(w):
        for j in range(h):
            lbl_reshaped[i][j] = labels[labels_idx]
            labels_idx += 1
    return lbl_reshaped
