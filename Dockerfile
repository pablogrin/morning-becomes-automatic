FROM public.ecr.aws/lambda/python:3.7

COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY src/ ./

CMD [ "lambda_function.handler" ]