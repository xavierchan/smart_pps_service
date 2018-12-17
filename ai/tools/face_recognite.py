# coding: utf-8

import face_recognition


class FaceRecognite(object):

    def get_encodings(self, file):
        encodings = face_recognition.face_encodings(
            face_recognition.load_image_file(file)
        )
        return encodings[0]

    def find_target(self, name):
        print '开始匹配【{name}】'.format(name=name)
        target_path = './target/'
        target = self.get_encodings('{base}{name}.jpeg'.format(
            base=target_path, name=name)
        )
        results = []
        pics_encodings = self.get_pics_encodings()
        results = face_recognition.compare_faces(
            pics_encodings.values(), target, tolerance=0.55
        )
        results = [k for k, v in dict(zip(pics_encodings.keys(), results)).iteritems() if v]
        return results

    def get_pics_encodings(self):
        base_path = './pics/'
        sources = []
        face_sources = {}
        for root, dirs, files in os.walk(base_path, topdown=False):
            for name in files:
                if os.path.splitext(name)[1] in ['.jpg', '.png', '.jpeg']:
                    sources.append(base_path + name)
        for source in sources:
            encodings = self.get_encodings(source)
            if len(encodings) > 0:
                user_name = os.path.splitext(source)[0].replace(base_path, '')
                face_sources[user_name] = encodings
        return face_sources
