from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, TextAreaField, IntegerField, FormField, RadioField, SelectField, SelectMultipleField, FloatField, validators
from wtforms.validators import DataRequired, Length

# import pdb; pdb.set_trace()

def _validaCamposObrigatorios(campos):
    isvalid = True

    for campo in campos:
        if campo.data is None or (isinstance(campo.data, list) and not campo.data):
            campo.errors.append('This field is required.')
            isvalid = False

    if not isvalid:
        return False
    return True

def _validaCamposNaoNegativos(campos):
    isvalid = True

    for campo in campos:
        if campo.data < 0:
            campo.errors.append('This field cannot be negative.')
            isvalid = False

    if not isvalid:
        return False
    return True

def _validaRange(inicial, final, step):
    isvalid = inicial.data < final.data
    if not isvalid:
        inicial.errors.append('Invalid initial and final.')

    isvalid = step.data > 0 and step.data <= final.data - inicial.data
    if not isvalid:
        step.errors.append('Invalid step.')

    if inicial.errors or final.errors or step.errors:
        return False
    return True

class HyperInputIntForm(FlaskForm):
    fixedOrRange = RadioField('', choices=[('fixed','Fixed'),('range','Range')], default='fixed', validators=[DataRequired()])
    fixo = IntegerField('Fixo', [validators.optional()])
    inicial = IntegerField('Inicial', [validators.optional()])
    final = IntegerField('Final', [validators.optional()])
    step = IntegerField('Step', [validators.optional()])

    def __init__(self, *args, **kwargs):
        kwargs["csrf_enabled"] = csrf_enabled = False
        FlaskForm.__init__(self, *args, **kwargs)

    def validate(self):
        if not FlaskForm.validate(self):
            return False

        isvalid = True

        if self.fixedOrRange.data == 'fixed':
            campos = [self.fixo]
            isvalid = isvalid and _validaCamposObrigatorios(campos) and _validaCamposNaoNegativos(campos)
        else:
            campos = [self.inicial,self.final,self.step]
            isvalid = isvalid and _validaCamposObrigatorios(campos) and _validaCamposNaoNegativos(campos)
            isvalid = isvalid and _validaRange(*campos)

        return isvalid

    def getData(self):
        if self.fixedOrRange.data == 'fixed':
            return self.getFixed()
        else:
            return self.getRange()

    def getRange(self):
        return self.inicial.data, self.final.data, self.step.data

    def getFixed(self):
        return self.fixo.data

class HyperInputFloatForm(FlaskForm):
    fixedOrRange = RadioField('', choices=[('fixed','Fixed'),('range','Range')], default='fixed', validators=[DataRequired()])
    fixo = FloatField('Fixo', [validators.optional()])
    inicial = FloatField('Inicial', [validators.optional()])
    final = FloatField('Final', [validators.optional()])
    step = FloatField('Step', [validators.optional()])

    def __init__(self, *args, **kwargs):
        kwargs["csrf_enabled"] = csrf_enabled = False
        FlaskForm.__init__(self, *args, **kwargs)

    def validate(self):
        if not FlaskForm.validate(self):
            return False

        isvalid = True

        if self.fixedOrRange.data == 'fixed':
            campos = [self.fixo]
            isvalid = isvalid and _validaCamposObrigatorios(campos) and _validaCamposNaoNegativos(campos)
        else:
            campos = [self.inicial,self.final,self.step]
            isvalid = isvalid and _validaCamposObrigatorios(campos) and _validaCamposNaoNegativos(campos)
            isvalid = isvalid and _validaRange(*campos)

        return isvalid

    def getData(self):
        if self.fixedOrRange.data == 'fixed':
            return self.getFixed()
        else:
            return self.getRange()

    def getRange(self):
        return self.inicial.data, self.final.data, self.step.data

    def getFixed(self):
        return self.fixo.data

class HyperInputDiscreteForm(FlaskForm):
    fixedOrMultiple = RadioField('', choices=[('fixed','Fixed'),('multiple','Multiple')], default='fixed', validators=[DataRequired()])
    fixo = SelectField('Fixo', choices=[('vazio','vazio')], validators=[validators.optional()])
    multiple = SelectMultipleField('Multiple', choices=[('vazio','vazio')], validators=[validators.optional()])

    def __init__(self, *args, **kwargs):
        kwargs["csrf_enabled"] = csrf_enabled = False
        FlaskForm.__init__(self, *args, **kwargs)

    def validate(self):
        # import pdb; pdb.set_trace()
        if not FlaskForm.validate(self):
            return False

        isvalid = True

        if self.fixedOrMultiple.data == 'fixed':
            campos = [self.fixo]
            isvalid = isvalid and _validaCamposObrigatorios(campos)
        else:
            campos = [self.multiple]
            isvalid = isvalid and _validaCamposObrigatorios(campos)

        return isvalid

    def getData(self):
        if self.fixedOrMultiple.data == 'fixed':
            return self.getFixed()
        else:
            return self.getMultiple()

    def getMultiple(self):
        return self.multiple.data

    def getFixed(self):
        return self.fixo.data

    def setChoices(self, choices):
        self.fixo.choices = self.multiple.choices = choices

class HyperparameterSettingForm(FlaskForm):

    batchOrSingle = RadioField('', choices=[('single','Add single block'),('batch','Add a batch of blocks')], default='single', validators=[DataRequired()])

    split_size = IntegerField('Split Size', [validators.optional()], default=10)

    batch = FormField(HyperInputIntForm, description="Batch", default=100)
    epoch = FormField(HyperInputIntForm, description="Epoch", default=10)

    learn_rate = FormField(HyperInputFloatForm, description="Learning Rate", default=0.001)
    momentum = FormField(HyperInputFloatForm, description="Momentum", default=0.001)

    optimizer = FormField(HyperInputDiscreteForm, description="Optimizer")
    init_mode = FormField(HyperInputDiscreteForm, description="Init Mode")

    def __init__(self, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)
        # self.optimizer.setChoices([('SGD','SGD'),('RMSprop','RMSprop'),('Adagrad','Adagrad'),('Adadelta','Adadelta'), \
        #             ('Adam','Adam'),('Adamax','Adamax'),('Nadam','Nadam')])

        self.optimizer.setChoices([('SGD','SGD')])

        self.init_mode.setChoices([('uniform','uniform'),('lecun_uniform','lecun_uniform'),('normal','normal'),('zero','zero'), \
                    ('glorot_normal','glorot_normal'),('glorot_uniform','glorot_uniform'),('he_normal','he_normal'),('he_uniform','he_uniform')])

    def validate(self):
        if not FlaskForm.validate(self):
            return False

        isvalid = True

        if self.batchOrSingle.data == 'batch':
            campos = [self.split_size]
            isvalid = isvalid and _validaCamposObrigatorios(campos) and _validaCamposNaoNegativos(campos)

        return isvalid

    def batchMode(self):
        return self.batchOrSingle.data=="batch"
