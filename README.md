# N-Body-Problem

![Alt Text](./nbp.gif)

## set-up environment

> set access rights

```
chmod a+x run.sh
chmod a+x dependencies.sh
```

> virtual environment

```
python3 -m venv .
```

```
source ./bin/activate
```

> install dependecies 

```
./dependencies.sh
```

## tests on host

```
./run.sh
```

## run accelerator on Z2

> follow the [accelerator directory](./Accelerator/)

> > on low spec machines - this system will at the least `4X` the native python implementation