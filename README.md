# kabu.com API�p�R�[�h

## ���O����

- au�J�u�R���،��̌������
  - https://kabu.com/

- kabu�X�e�[�V�����i�ʏ�v�����j �ɐ\������ŃA�v�����_�E�����[�h����
  - https://kabu.com/kabustation/
  - kabu�X�e�[�V�����i�{�́j�͗��p���� 990�~�i�ō��j/�� �����A�M�p�����J�ݍς݂̏ꍇ���� �Ȃ̂ŐM�p�����J�݂���Ƃ����i�M�p�����J�݂͑����Œʂ����j



## ���s�菇

#### 0.kabu�X�e�[�V�����̃A�v���N�����Ă���
**���A�v���N�����Ă����Ȃ���api�g���Ȃ�**

#### 1.token�擾
**��../../auth.yaml �����Ă����K�v����I�I�I�I**

```
python get_token.py
-> �J�����g�f�B���N�g���� token.yaml ���o�͂����
```

#### 2.�������擾
```
python kabusapi_symbol.py -s 5401 -o output_tmp
-> �������Ƃ��� output_tmp/kabusapi_symbol_5401.csv ���o�͂����
```

#### 3.kabu�X�e�[�V�����ɖ����o�^
�������R�[�h�Ǝs��R�[�h��2.�������擾��csv����킩��
���o�^����������kabu�X�e�[�V�����̉E���<>����m�F�ł���
```
python kabusapi_register.py -s 5401 -e 1
```

#### 4.���������i�����j��/��
```
python kabusapi_sendorder_cash.py -i input_tmp/input_kabusapi_sendorder_cash.csv
-> input_tmp/input_kabusapi_sendorder_cash1.csv �̒��������s�����
```

#### 5.kabu�X�e�[�V�����̓o�^�����̃��A���^�C���̏����擾����
��9-15���̊Ԃ���Ȃ��Ǝg���Ȃ�
��kabu�X�e�[�V�����ɖ����o�^���Ă����Ȃ��Ǝg���Ȃ�
```
python kabusapi_websocket.py
```

#### 5-1.���A���^�C����kabu�X�e�[�V�����̓o�^�����̒���������
������csv�K�v
��kabu�X�e�[�V�����ɖ����o�^���Ă����Ȃ��Ǝg���Ȃ�
```
python kabusapi_websocket.py -i input_tmp/input_kabusapi_sendorder_cash.csv
```


