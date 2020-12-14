import os
import json
import argparse

present_classes = [1, 10, 25, 28, 29, 40, 41, 43, 44, 45, 66, 68, 74, 78, 80]
annotated_classes = [1]

parser = argparse.ArgumentParser(
    description='JSON parser')
parser.add_argument('--json_in', default='./data/example.json', type=str)
parser.add_argument('--json_out', default='./data/result.json', type=str)
args = parser.parse_args()
json_in = args.json_in
json_out = args.json_out

with open(json_in, 'r') as f:
    in_dset = json.load(f)

out_dset = in_dset.copy()

print('From ' + str(len(in_dset['images'])) + ' images and ' + str(len(in_dset['annotations'])) + ' annotated objects')

valid_ids = [annot_valid['image_id'] for annot_valid in in_dset['annotations']
             if annot_valid['category_id'] in present_classes]
valid_imgs = [img_valid for img_valid in in_dset['images'] if img_valid['id'] in valid_ids]
valid_annotations = [annot_valid for annot_valid in in_dset['annotations'] if annot_valid['image_id'] in valid_ids]
for iva in range(len(valid_annotations)):
    valid_annotations[iva]['category_id'] = 500 if valid_annotations[iva]['category_id'] not in annotated_classes \
        else valid_annotations[iva]['category_id']

print(str(len(valid_imgs)) + ' images')
print(str(len(valid_annotations)) + ' annotated objects')

out_dset['images'] = valid_imgs
out_dset['annotations'] = valid_annotations

with open(json_out, 'w') as f:
    json.dump(out_dset, f)