
class Opt:
    conf_path = "config/conf.yaml"
    test_var1 = "foo"

    @staticmethod
    def info():
        return "class Opt:\n\t" + "\n\t".join([x + ": " + str(getattr(Opt, x)) for x in dir(Opt) if (x[0]!="_" and x[-1]!="_")])