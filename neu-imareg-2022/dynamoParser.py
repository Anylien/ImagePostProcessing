#  08/28/2019
#
#  dynamoParser.py
#  
#  Bastien HARMAND <bastien.harmand@mines-ales.org>

import boto3
from boto3.dynamodb.types import Decimal
boto3.setup_default_session(profile_name='default')


class DynamoDB:

    """
    DynamoDB data parsing
    """

    # Initiate the connection with dynamodb
    def __init__(self, table_name, region):
        self.table_name = table_name
        self.region = region
        self.dynamodb = boto3.resource('dynamodb', region_name=region)
        self.dynamodb_table = self.dynamodb.Table(table_name)

    # Return one item by primary key
    def read_item(self, pk_name1, pk_value1, pk_name2, pk_value2):
        return self.dynamodb_table.get_item(Key={pk_name1: pk_value1, pk_name2: pk_value2})
        # return self.dynamodb_table.get_item(Key={pk_name1: pk_value1})

    # Write the ajdustements to correct the coordinates
    def write_translations(self, uid, job_id, tx, ty, scale, output_key):
        result = self.read_item("keypri", uid, "idj", job_id)['Item']
        content = {}
        if 'imareg' in result:
            content = result['imareg']
        output_content = {'trasca': Decimal(str(scale)), 'tracox': tx, 'tracoy': ty}
        content[output_key] = output_content
        self.dynamodb_table.update_item(TableName=self.table_name, Key={'keypri': uid, 'idj': job_id},
                                        UpdateExpression="set imareg=:imareg",
                                        ExpressionAttributeValues={":imareg": content})

    # Write the picture dimensions
    def write_image_size(self, uid, job_id, width, height, output_key):
        result = self.read_item("keypri", uid, "idj", job_id)['Item']
        content = {}
        if 'imareg' in result:
            content = result['imareg']
            if output_key in content:
                content[output_key]['wid'] = width
                content[output_key]['hei'] = height
            else:
                content[output_key] = {'wid': width, 'hei': height}
        else:
            output_content = {'wid': width, 'hei': height}
            content[output_key] = output_content
        self.dynamodb_table.update_item(TableName=self.table_name, Key={'keypri': uid, 'idj': job_id},
                                        UpdateExpression="set imareg=:imareg",
                                        ExpressionAttributeValues={":imareg": content})

    # Write the technical points
    def write_technical_points(self, uid, job_id, bll_left_x, bll_left_y, blr_left_x, blr_left_y, bll_right_x,
                               bll_right_y, blr_right_x, blr_right_y, use_left, use_right, output_key):
        result = self.read_item("keypri", uid, "idj", job_id)['Item']
        content = {}
        if 'imareg' in result:
            content = result['imareg']
        if use_left and use_right:
            output_content = {'tpo-bll-lft-spf-coo': {'cox': bll_left_x, 'coy': bll_left_y},
                              'tpo-blr-lft-spf-coo': {'cox': blr_left_x, 'coy': blr_left_y},
                              'tpo-bll-rgh-spf-coo': {'cox': bll_right_x, 'coy': bll_right_y},
                              'tpo-blr-rgh-spf-coo': {'cox': blr_right_x, 'coy': blr_right_y}}
        elif use_left:
            output_content = {'tpo-bll-lft-spf-coo': {'cox': bll_left_x, 'coy': bll_left_y},
                              'tpo-blr-lft-spf-coo': {'cox': blr_left_x, 'coy': blr_left_y}}
        else:
            output_content = {'tpo-bll-rgh-spf-coo': {'cox': bll_right_x, 'coy': bll_right_y},
                              'tpo-blr-rgh-spf-coo': {'cox': blr_right_x, 'coy': blr_right_y}}
            
        content[output_key]['tecpoldat'] = output_content
        self.dynamodb_table.update_item(TableName=self.table_name, Key={'keypri': uid, 'idj': job_id},
                                        UpdateExpression="set imareg=:imareg",
                                        ExpressionAttributeValues={":imareg": content})

    # Read multiples objects with one reponse
    def read_meta(self, uid, job_id):
        response = self.read_item('keypri', uid, 'idj', job_id)
        return self.read_bounding_box(uid, job_id, response), self.read_view(uid, job_id, response), self.read_exercice(uid, job_id, response)

    # Return the body bounding box
    def read_bounding_box(self, uid, job_id, response=None):
        if response is None:
            response = self.read_item('keypri', uid, 'idj', job_id)
        bounding_box = response['Item']['ContentLab']['BoundingBox']
        return float(bounding_box['Width']), float(bounding_box['Height']), float(bounding_box['Left']), float(bounding_box['Top'])

    # Read the position (x and y) of a body keypoint
    def read_keypoint_pos(self, uid, job_id, keypoint_name, response=None):
        if response is None:
            response = self.read_item('keypri', uid, 'idj', job_id)
        keypoint = response['Item']['jsokeypo1']['bodkrt']['bodmardat'][keypoint_name]
        return int(keypoint['cox']), int(keypoint['coy'])

    # Read the view of the scene (ant, pos, sin or dex)
    def read_view(self, uid, job_id, response=None):
        if response is None:
            response = self.read_item('keypri', uid, 'idj', job_id)
        return response['Item']['typvie']

    # Read the exercice done on the scene (ups,rls,lls,etc...)
    def read_exercice(self, uid, job_id, response=None):
        if response is None:
            response = self.read_item('keypri', uid, 'idj', job_id)
        return response['Item']['typexe']
