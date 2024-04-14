import random


class __Lorem:
    LOREM_IPSUM = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin id luctus lorem, vel tincidunt nibh. Curabitur sodales eros vitae massa finibus, vestibulum sagittis erat iaculis. In vel dui ac tortor faucibus elementum eu id sem. Nam id nibh nec eros placerat dapibus. Pellentesque varius, lectus non sodales suscipit, ex turpis laoreet risus, ut molestie ex enim eget mi. Duis vestibulum, diam vitae commodo rutrum, nibh ligula pharetra est, congue fringilla turpis lacus ac risus. Sed gravida viverra dui semper dignissim. Vivamus imperdiet nunc eget nunc lobortis, vehicula ornare lectus euismod. Nulla aliquam purus nisl, at elementum nisl bibendum eu. Ut congue posuere risus, sit amet porttitor lacus placerat nec. Duis hendrerit eget augue ac consequat. Integer vel eleifend tellus. Praesent consectetur elit odio, at accumsan felis tincidunt ac. Nullam convallis urna ante, venenatis dignissim urna condimentum tempor. Nulla sed nisi eu nisl facilisis placerat. Vivamus id ipsum accumsan, interdum enim id, tincidunt purus. Fusce ac faucibus tellus, non feugiat neque. Nunc eget mattis arcu, sed vulputate magna. Quisque ornare ex nec enim elementum rutrum. Praesent venenatis ante et augue fringilla efficitur. Nullam rutrum tincidunt dolor, pellentesque mattis justo venenatis eu. Etiam venenatis tincidunt ex, auctor mattis quam interdum sed. Sed rhoncus, sem sit amet consectetur venenatis, magna orci suscipit arcu, non auctor erat augue eu diam. Cras facilisis non ipsum ut lobortis. Suspendisse condimentum lacus vel purus molestie hendrerit. Etiam ultrices nunc ut mauris mollis venenatis non a erat. Maecenas ut odio sapien. Duis et diam nibh. Etiam sed cursus nibh. Praesent convallis, eros ut pulvinar blandit, dui dolor aliquet odio, id pellentesque turpis nulla vitae nibh. Sed id ante eu mauris cursus varius. Fusce libero magna, condimentum ultricies fermentum vitae, tincidunt sed tellus. Vivamus sollicitudin orci orci, ut fermentum magna iaculis vel. Donec placerat mauris sed sagittis aliquam. Nulla in orci ut mi vestibulum fermentum quis eget nibh. Donec consectetur lectus eget lacus lacinia, quis dignissim leo tempor. Duis tempus enim sit amet est tempus, a ultricies dolor condimentum. Cras vel ultrices lacus, et pretium elit. Nunc quis convallis enim. Donec pharetra eros massa, aliquam accumsan diam mollis quis. In in posuere turpis, vel eleifend ante. Sed at nunc sed neque auctor ullamcorper. Vestibulum porttitor, tellus ac auctor ultricies, magna nisi lacinia mi, ut dignissim ex enim euismod mi. Phasellus pellentesque, augue vitae ultricies dignissim, eros mi luctus est, eu ullamcorper mauris nunc in lacus. Duis feugiat finibus mauris id ullamcorper. Sed tristique convallis ligula. Integer eu erat pretium neque commodo auctor et nec mi."

    def __init__(self):
        self.sentences = []
        self.parts = []
        for sentence in self.LOREM_IPSUM.split("."):
            sentence = sentence.strip()
            if sentence == "":
                continue
            self.sentences.append(sentence)
            for part in sentence.split(","):
                self.parts.append(part.strip())

    def get_sentence(self, max_length):
        sentence = random.choice(self.sentences)
        words = sentence.split(" ")
        output = ""
        for word in words:
            if len(output) + len(word) > max_length:
                return output
            if len(output) > 0:
                output += " "
            output += word
        return output


__lorem = __Lorem()


def ipsum(max_length=50):
    return __lorem.get_sentence(max_length)
