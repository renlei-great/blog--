import setuptools
import glob

print(glob.glob('*.py'))

setuptools.setup(
    name="blog",  # Replace with your own username
    version="0.0.1",
    author="renlei",
    author_email="rl1415977534@163.com",
    description="magedu react django blog",
    url="https://github.com/pypa/sampleproject",
    packages=['blog', 'post', 'user'],
    data_files=['requeirements', 'manage.py'],  # ('tempaltes/*.html')
)

# 　使用命令　python setup.py sdist　就可进行打包分发源码
